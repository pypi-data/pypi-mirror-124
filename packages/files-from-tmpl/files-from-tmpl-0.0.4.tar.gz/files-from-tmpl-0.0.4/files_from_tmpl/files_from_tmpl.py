from pathlib import Path
import shutil
import jinja2


def generate(
    src: str = 'template', dst_dir: str = '.',
    *, dst_name: str = 'output', rewrite: bool = False, **kwargs,
) -> None:
    """Generate file structure from src to dst_dir/dst_name.
    Transform src names with str.format(**kwargs). Render .tmpl files with jinja2.

    Args:
        src (path-like object) - source file or directory
        dst_dir (path-like object) - destination directory
        dst_name (str) - destination object name;
            if empty then calculates from src;
            final value adds to kwargs
        rewrite (bool) - allows to rewrite existing objects
    """

    src, dst_dir = Path(src), Path(dst_dir)

    if not (src.is_dir() or src.is_file()):
        raise ValueError(f'src="{src}" must point to directory or regular file!')

    try:
        dst_dir.mkdir(parents=True, exist_ok=True)
    except FileExistsError:
        raise ValueError(
            f'dst_dir="{dst_dir}" must not point to existing non-directory file!')

    if not dst_name:
        dst_name = calculate_dst_name(src, kwargs)
    kwargs['dst_name'] = dst_name

    dst = dst_dir / dst_name

    if dst == src:
        raise ValueError(f'dst="{dst}" must not be the same as src!')

    if dst.exists():
        if rewrite:
            if dst.is_dir():
                shutil.rmtree(dst)
            elif dst.is_file():
                dst.unlink()
            else:
                raise ValueError(f'Unable to replace the file "{dst}"!')
        else:
            raise ValueError(f'dst="{dst}" is alredy exists!')

    continue_generation(src, dst, kwargs)


def calculate_dst_name(src: Path, kwargs: dict) -> str:
    if is_tmpl(src):
        src_name = src.stem
    else:
        src_name = src.name

    return src_name.format(**kwargs)


def is_tmpl(src: Path) -> bool:
    return src.is_file() and (src.suffix == '.tmpl')


def continue_generation(src: Path, dst: Path, kwargs: dict) -> None:
    if src.is_file():
        if is_tmpl(src):
            env = jinja2.Environment(
                loader=jinja2.FileSystemLoader(src.parent),
                keep_trailing_newline=True,
            )
            template = env.get_template(src.name)
            with open(dst, 'w') as f:
                f.write(template.render(kwargs))
        else:
            shutil.copy(src, dst)

    elif src.is_dir():
        dst.mkdir(exist_ok=True)
        for next_src in src.iterdir():
            next_dst = dst / calculate_dst_name(next_src, kwargs)
            continue_generation(next_src, next_dst, kwargs)
