from pathlib import Path

from imxIcons.iconService import ICON_DICT, IconService, ImxVersionEnum
from imxIcons.iconServiceModels import IconRequestModel


async def create_asset_folder(base_dir: Path = Path(__file__).parent):
    base_path = Path(base_dir / "static")
    base_path.mkdir(parents=True, exist_ok=True)

    folder_dict = {}
    for folder in [_.name for _ in ImxVersionEnum]:
        imx_version_folder = base_path / folder
        imx_version_folder.mkdir(parents=True, exist_ok=True)
        folder_dict[folder] = imx_version_folder

    for imx_path, versions in ICON_DICT.items():
        for version, icons in versions.items():
            icon_folder_base = folder_dict[version]

            for icon in icons:
                svg_content = IconService.get_svg(
                    IconRequestModel(
                        imx_path=icon.imx_path, properties=icon.properties
                    ),
                    ImxVersionEnum[version],
                )
                file_path = icon_folder_base / f"{icon.icon_name}.svg"
                file_path.write_text(svg_content, encoding="utf-8")