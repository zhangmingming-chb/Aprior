#-*-coding:utf-8-*-
from typing import List
from itertools import chain

class Aprior():

    def __init__(self, support, confidence):
        self.support = support
        self.confidence = confidence

    def set_transactions(self, transactions: List[List[str]]) -> None:
        self.transactions = transactions

    def get_I(self) -> List[str]:
        return sorted(set(chain(*self.transactions)))

    def F(self, items: List[List[str]] or List[str]) -> List[List[str]]:
        # 统计集合出现次数
        records = {}
        query_table = {}
        for i in items:
            for j in self.transactions:
                query_table[id(i)] = i
                if set(i).issubset(set(j)):
                    if id(i) not in records:
                        records[id(i)] = 1
                    else:
                        records[id(i)] += 1
        # 选出k-频繁项集
        item = []
        for k, v in records.items():
            if v / len(self.transactions) >= self.support:
                item.append(query_table[k])
        item = list(map(lambda x: sorted(list(x)), item))
        return item

    def generate_1_items(self, I: List[str]) -> List[List[str]]:
        return self.F(I)

    def generate_k_items(self, k_last_items: List[List[str]]) -> List[List[str]]:
        prefix = []
        for i in k_last_items:
            prefix.append(",".join(i[:-1]))

        records = {}
        for i in prefix:
            records[i] = []

        for i in k_last_items:
            # 将只有最后一个元素不同的集合分组
            current_prefix = ",".join(i[:-1])
            if current_prefix in records.keys():
                records[current_prefix].append(i)

        items = []
        for v in records.values():
            for i in range(len(v)):
                for j in range(i + 1, len(v)):
                    temp = sorted(list(set(v[i]).union(v[j])))
                    # 判断集合中的后k-1是否在k-1-频繁项集中
                    if temp[1:] in k_last_items:
                        items.append(temp)
        return self.F(items)

    def k_items_result(self) -> List[List[str]]:
        I = self.get_I()
        items = self.generate_1_items(I)
        item_max_length = len(sorted(self.transactions,key=lambda x:len(x))[-1])
        while True:
            if len(items) == 1 or len(items[0]) > item_max_length:
                break
            last_items = items[::]
            items = self.generate_k_items(items)
            # 无符合的频繁项集，返回上次计算结果
            if len(items) == 0:
                return last_items
        return items

tran = [
    ['1','2','3'],
    ['1','2','4'],
    ['1','3','4'],
    ['1','2','3','5'],
    ['1','3','5'],
    ['2','4','5'],
    ['1','2','3','4']
]

# tran = [
#     ['apple','banana','orange'],
#     ['apple','banana','peer'],
#     ['apple','orange','peer'],
#     ['apple','banana','orange','mongo'],
#     ['apple','orange','mongo'],
#     ['banana','peer','mongo'],
#     ['apple','banana','orange','peer']
# ]

ap = Aprior(support=3/7,confidence=5/7)
ap.set_transactions(tran)

print(ap.k_items_result()) # [['1', '2', '3']]

