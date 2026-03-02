from pathlib import Path
import re
import ast
import textwrap

BEGIN = "# BEGIN_AUTOGEN"

END = "# END_AUTOGEN"

# these index the start and end of the region within presets.py for which stuff will be overwritten by this module
 


def _find_autogen_region(text: str) -> tuple[int, int, int, int]:
    b0 = text.find(BEGIN)
    e0 = text.find(END)
    #identify the relevant part of the text
    if b0 == -1 or e0 == -1 or e0 < b0:
        raise RuntimeError("Missing or malformed AUTOGEN region markers in presets.py")

    # content starts after the END of the BEGIN marker line
    b_line_end = text.find("\n", b0)
    if b_line_end == -1:
        #obviously these cases would indicate somethin wrong with the format of the presets.py file, so we should raise an error instead of silently doing nothing or worse, overwriting the whole file
        raise RuntimeError("BEGIN_AUTOGEN marker line has no newline")
    # idenitfy text up to and before the marker
    begin_content_start = b_line_end + 1
    end_marker_end = text.find("\n", e0)
    # and text after the end marker
    if end_marker_end == -1:
        end_marker_end = len(text)
    else:
        end_marker_end += 1

    return b0, begin_content_start, e0, end_marker_end

def write_autogen_functions(presets_path: str, functions_src: str) -> None:
    p = Path(presets_path)
    text = p.read_text(encoding="utf-8")
    # get the overwrite region from the function
    _, begin_content_start, end_marker_start, _ = _find_autogen_region(text)

    before = text[:begin_content_start]
    after = text[end_marker_start:]

    body = functions_src.rstrip() + "\n"
    # new text is the same as old, but with the content between the markers replaced by the new function source
    new_text = before + body + after
    # write new text to the file, overwriting the old content
    p.write_text(new_text, encoding="utf-8")

def upsert_autogen_function(presets_path: str, func_src: str) -> None:
    """
    Basically go inside the autogen region, look for a function with the given name youre trying to write.
    If it exists, replace it with the new source. If it doesn't exist, append the new function source to the end of the region.
    for overwriting presets >:(|)
    
    """
    src = textwrap.dedent(func_src).lstrip()
    mod = ast.parse(src)

    defs = [n for n in mod.body if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))]
    if len(defs) != 1:
        raise ValueError(f"Expected exactly 1 top-level function in func_src, found {len(defs)}")
    func_name = defs[0].name

    p = Path(presets_path)
    text = p.read_text(encoding="utf-8")

    _, begin_content_start, end_marker_start, _ = _find_autogen_region(text)
    # get the text before the content, the content, and the text after the content, so we can reconstruct the file after modifying the content

    before = text[:begin_content_start]
    block = text[begin_content_start:end_marker_start] #block containing presets
    after = text[end_marker_start:]

    lines = block.splitlines(keepends=True) # breaks the block into separate lines keeps the \n (keepends=True) so we can reconstruct the block after modifying it

    def_pat = re.compile(r"^def\s+([A-Za-z_]\w*)\s*\(", re.ASCII) #regex pattern that matches the start of a top-level Python function definition line
    target_pat = re.compile(rf"^def\s+{re.escape(func_name)}\s*\(", re.ASCII) #regex pattern that matches the start of a top-level Python function definition line


    start = None
    for i, line in enumerate(lines):
        if target_pat.match(line):
            start = i
            break
    #above looks for the start of the preset function we're tryna right @:)

    func_src_norm = func_src.rstrip() + "\n" #func_src is our new preset function. we want to remove the new lines and replace with \n.
    func_lines = func_src_norm.splitlines(keepends=True)#converts new string into a list of lines. keeeps \n

    if start is None: #if it doesnt exist, add it to the end of the block
        # append (ensure one blank line separation if block isn't empty)
        if lines and not (lines[-1].endswith("\n") and lines[-1].strip() == ""): #lines are the lines already in our preset file. if there are any lines, and the last line isn't blank, add a blank line before appending the new function
            if lines[-1].strip() != "":#check if the last line isn't already blank (if it has non-whitespace characters), then add a blank line
                lines.append("\n")
        lines.extend(func_lines) #add our new function to the end of the block
    else:#if it exists, overwrite it
        # find end: next top-level def, or end of block
        end = len(lines) #the latest our current version of the function could end is the end of the block.
        for j in range(start + 1, len(lines)): #iterate through the lines after the start of the function we're replacing, looking for the next top level function definition i.e the next def Preset_Name which we identify using def_pat
            if def_pat.match(lines[j]):
                end = j #if it a new function starts this is the end
                break
        lines[start:end] = func_lines #replace previous function preset with our new function preset by replacing the lines from start to end with the lines of our new function

    new_block = "".join(lines)
    new_text = before + new_block + after
    p.write_text(new_text, encoding="utf-8")

# Example: generate one function

fn = """\

def STIRAP():

    return dict(

        name="STIRAP",

        duration=5.0,

        dds_functions={

            "397a": gaussian(mu=1.0, sigma=2.0),

            "866": gaussian(mu=1.0, sigma=3.5),

        },

        pmt_gate_high=True,

    )

"""
 
upsert_autogen_function("presets_test.py", fn)

 