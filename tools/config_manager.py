from pathlib import Path

def get_config_paths(project_root, model_name):
    project_dir = project_root / f"docs/{model_name}/source"
    build_dir = project_root / f"docs/{model_name}/build"
    return project_dir, build_dir
