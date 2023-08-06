from dataclasses import dataclass, field
from vuabl.data.asset import Asset


@dataclass
class AssetData:
    asset: Asset = Asset()
    size: int = 0
    referencedByAssets: set = field(default_factory=set)
    referencedByGroups: set = field(default_factory=set)
    referencedByArchives: set = field(default_factory=set)
