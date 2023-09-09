attribute_types = {'site': 'str',
                   'year': 'int',
                   'decid_frac': 'float'}

trn_data = list()

print('Total {} sites'.format(str(len(out_decid_frac_samp))))

ntrn = int((trn_perc * len(out_decid_frac_samp)) / 100.0)
nval = len(out_decid_frac_samp) - \
       ntrn

# randomly select training samples based on number
trn_sites = Sublist(range(len(out_decid_frac_samp))).random_selection(ntrn)

# get the rest of samples as validation samples
val_sites = Sublist(range(len(out_decid_frac_samp))).remove(trn_sites)

# print IDs
print(len(trn_sites))
print(len(val_sites))

wkt_list = list()
attr_list = list()

trn_wkt_list = list()
trn_attr_list = list()

val_wkt_list = list()
val_attr_list = list()

for i, row in enumerate(out_decid_frac_samp):
    elem = dict()

    for header in list(attribute_types):
        elem[header] = row[header]

    wkt = Vector.wkt_from_coords([row['longitude'], row['latitude']],
                                 geom_type='point')

    if i in trn_sites:
        trn_wkt_list.append(wkt)
        trn_attr_list.append(elem)
    elif i in val_sites:
        val_wkt_list.append(wkt)
        val_attr_list.append(elem)

    wkt_list.append(wkt)
    attr_list.append(elem)