def displayInventory(inventory):
    if(inventory is None or len(inventory)==0):
        print('Inventory is empty')
        return None
    else:
        objectCount = 0
        print('Inventory:')
        for k, v in inventory.items():
            objectCount += v #count the objects
            print(str(v) + ' ' + str(k))
        print('Total number of items: ' + str(objectCount))

def addToInventory(inventory, addedItems):
    for element in dragonLoot:
        if element in inventory.keys():
            inventory[element]+=1
        else:
            inventory.setdefault(element,1)
    return inventory

inv = {'gold coin': 42, 'rope': 1}
dragonLoot = ['gold coin', 'dagger', 'gold coin', 'gold coin', 'ruby']
inv = addToInventory(inv, dragonLoot)
displayInventory(inv)
