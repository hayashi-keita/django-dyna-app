from multiprocessing import process
from production_plan.models import ProductProcess, OrderItemProcess

# 工程展開処理
def expand_process_for_order_item(order_item):
    # 既に展開済みか確認
    existing = OrderItemProcess.objects.filter(order_item=order_item)
    # すでにplanningまたはcompletedがある場合は展開禁止
    if existing.filter(status__in=['planning', 'completed']).exists():
        return False
    # pending のみ再展開（古い pending は削除）
    existing.filter(status='pending').delete()
    
    product_processes = ProductProcess.objects.filter(product=order_item.product).order_by('sequence')

    new_processes = [
        OrderItemProcess(
            order_item=order_item,
            process=pp.process,
            sequence=pp.sequence,
            status='draft'
        )
        for pp in product_processes
    ]
    OrderItemProcess.objects.bulk_create(new_processes)
    return True