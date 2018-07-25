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
    

inventory = {'toothbrush':1, 'axe':2, 'backpack':3, 'toy':0, 'memes':56}
displayInventory(inventory)
