from assets.pagination import AssetPaginationBase
from perms.models import UserAssetGrantedTreeNodeRelation
from common.utils import get_logger

logger = get_logger(__name__)


class NodeGrantedAssetPagination(AssetPaginationBase):
    def get_count_from_nodes(self, queryset):
        node = getattr(self._view, 'pagination_node', None)
        if node:
            logger.debug(f'Hit node.assets_amount[{node.assets_amount}] -> {self._request.get_full_path()}')
            return node.assets_amount
        else:
            logger.warn(f'Not hit node.assets_amount[{node}] because {self._view} not has `pagination_node` -> {self._request.get_full_path()}')
            return super().get_count(queryset)


class AllGrantedAssetPagination(AssetPaginationBase):
    def get_count_from_nodes(self, queryset):
        assets_amount = sum(UserAssetGrantedTreeNodeRelation.objects.filter(
            user=self._user, node_parent_key=''
        ).values_list('node_assets_amount', flat=True))
        logger.debug(f'Hit all assets amount {assets_amount} -> {self._request.get_full_path()}')
        return assets_amount
