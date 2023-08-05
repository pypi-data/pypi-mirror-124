# # -*- coding: utf-8 -*-
# # Python imports
# from promise import Promise
# from promise.dataloader import DataLoader
#
#
# # Django imports
#
# # 3rd Party imports
#
# # App imports
#
#
# class ModelDataLoader(DataLoader):
#     model = None
#
#     def batch_load_fn(self, keys):
#         order = sorted(xrange(len(keys)), key=lambda i: keys[i])
#         items = list(self.model.objects.filter(id__in=keys).order_by('pk'))
#         return Promise.resolve([items[order[keys.index(key)]] for key in keys])
