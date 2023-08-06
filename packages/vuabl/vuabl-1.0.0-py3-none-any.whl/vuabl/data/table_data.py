from pandas import DataFrame
from vuabl.data.group import Group
from vuabl.data.asset_data import AssetData
import vuabl.utils.conversion as conversion



def get_group_assets_table_by_size(group: Group, assetsData: dict) -> DataFrame:
    assetsData: list[AssetData] = list(assetsData.values())

    assetsData.sort(key=lambda entry:entry.size, reverse=True)

    paths: list[str] = [assetData.asset.path for assetData in assetsData]
    types: list[str] = [assetData.asset.assetType.name for assetData in assetsData]
    sizes: list[str] = [conversion.bytes_to_readable_size(assetData.size) for assetData in assetsData]

    references: list[str] = []

    for assetData in assetsData:
        referencedBy: list[str] = [referenceAsset.path for referenceAsset in assetData.referencedByAssets]
        referencedBy.sort()

        referencesStr: str = ""

        for index, reference in enumerate(referencedBy):
            if index > 0:
                referencesStr += "\n"

            referencesStr += reference

        references.append(referencesStr)

    return DataFrame(dict(path=paths, type=types, size=sizes, references=references))



def get_duplicates_table(assetsData: dict) -> DataFrame:
    duplicates: list[AssetData] = []

    for path, data in assetsData.items():
        if len(data.referencedByArchives) > 1:
            duplicates.append(data)

    duplicates.sort(key=lambda assetData: assetData.size * len(assetData.referencedByArchives), reverse=True)

    paths: list[str] = [assetData.asset.path for assetData in duplicates]
    sizes: list[str] = []
    groups: list[str] = []
    references: list[str] = []

    for assetData in duplicates:
        duplicatesCount: int = len(assetData.referencedByArchives)
        summedSize: int = duplicatesCount * assetData.size
        summedSizeStr: str = conversion.bytes_to_readable_size(summedSize)
        assetSizeStr: str = conversion.bytes_to_readable_size(assetData.size)
        sizeStr: str = f"{summedSizeStr} ({duplicatesCount}x{assetSizeStr})"
        sizes.append(sizeStr)

        groupsStr: str = ""
        referencedByGroups: list[str] = [group for group in assetData.referencedByGroups]
        referencedByGroups.sort()

        for index, group in enumerate(referencedByGroups):
            if index > 0:
                groupsStr += "\n"

            groupsStr += group

        groups.append(groupsStr)

        referencesStr: str = ""
        referencedByAssets: list[str] = [assetReference.path for assetReference in assetData.referencedByAssets]
        referencedByAssets.sort()

        for index, reference in enumerate(referencedByAssets):
            if index > 0:
                referencesStr += "\n"

            referencesStr += reference

        references.append(referencesStr)

    return DataFrame(dict(path=paths, size=sizes, groups=groups, references=references))
