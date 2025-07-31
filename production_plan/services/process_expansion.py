from multiprocessing import process
from production_plan.models import ProductProcess, OrderItemProcess

# 工程展開処理
def expand_process_for_order_item(order_item):
    # 既にplanningまたはcompletedがある場合は展開禁止
    existing = OrderItemProcess.objects.filter(order_item=order_item)
    if existing.filter(status__in=['planning', 'completed']).exists():
        return False
    # draftやpendingを削除して再展開
    existing.delete()
    
    product_processes = ProductProcess.objects.filter(
        product=order_item.product
        ).order_by('sequence')

    OrderItemProcess.objects.bulk_create([
        OrderItemProcess(
            order_item=order_item,
            process=pp.process,
            sequence=pp.sequence,
            status='pending'
        )
        for pp in product_processes
    ])
    return True