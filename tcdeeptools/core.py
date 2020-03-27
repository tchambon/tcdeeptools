# AUTOGENERATED! DO NOT EDIT! File to edit: 00_core.ipynb (unless otherwise specified).

__all__ = ['nb2script']

# Cell

def _is_export(cell):
    if cell['cell_type'] != 'code': return False
    src = cell['source']
    if len(src) == 0 or len(src[0]) < 7: return False
    #import pdb; pdb.set_trace()
    return re.match(r'^\s*#\s*export\s*$', src[0], re.IGNORECASE) is not None




# Credits to fastai/nbdev repository
def nb2script(nb_name, export_name):
    "Finds cells starting with `#export` and puts them into a new module"
    id_nb = int(nb_name.split('/')[-1].split('-')[0])
    fname = Path(nb_name)
    fname_out = f'nb{id_nb}-{export_name}.py'
    print(fname_out)
    main_dic = json.load(open(fname,'r',encoding="utf-8"))
    code_cells = [c for c in main_dic['cells'] if _is_export(c)]
    module = f'''
#################################################
### THIS FILE WAS AUTOGENERATED! DO NOT EDIT! ###
#################################################
# file to edit: ../{fname.name}
'''
    for cell in code_cells: module += ''.join(cell['source'][1:]) + '\n\n'
    # remove trailing spaces
    module = re.sub(r' +$', '', module, flags=re.MULTILINE)
    if not (fname.parent/'exp').exists(): (fname.parent/'exp').mkdir()
    output_path = fname.parent/'exp'/fname_out
    with io.open(output_path, "w", encoding="utf-8") as f:
        f.write(module[:-2])
    print(f"Converted {fname} to {output_path}")