from urllib.request import urlopen

class Item:
    def __init__(self, buy_average, sp, members, name, sell_average, overall_average, number, low_alch, high_alch):
        
        self._buy_average = buy_average
        self._sp = sp
        self._members = members
        self._name = name
        self._sell_average = sell_average
        self._overall_average = overall_average
        self._number = number
        self._low_alch = low_alch
        self._high_alch = high_alch
        self._ge_minus_high_alch = self._high_alch - self._sell_average

    def get_ge_minus_high_alch(self):
        return self._ge_minus_high_alch
    def get_high_alch(self):
        return self._high_alch
    def get_name(self):
        return self._name
    def get_buy_average(self):
        return self._buy_average
    def get_low_alch(self):
        return self._low_alch
    def get_members(self):
        return self._members
    def get_id(self):
        return self._number
    def get_overall_average(self):
        return self._overall_average
    def get_sp(self):
        return self._sp
    def get_sell_average(self):
        return self._sell_average
class Init:
    def __init__(self):
        #gathers all information from RSBuddy and the item tags and values table
        link = "https://rsbuddy.com/exchange/summary.json"
    
        f = urlopen(link)
        myfile = str(f.read())
        
        #omit leading {
        myfile = myfile[3:len(myfile)-1]

        #create list of items strings
        item_strings = []
        
        #load items
        i = 0
        while i < len(myfile):
            if myfile[i] == "{":
                start_index = i
                i += 1
            elif myfile[i] == "}":
                end_index = i
                item_strings.append(myfile[start_index + 1:end_index])
                myfile = myfile[end_index + 1:]
                i = 0
            else:
                i += 1
        
        
        #get alching info for all items
        file = open("alch_ids.txt", "r")
        
        file_lines = file.readlines()
        file_lines = file_lines[1:]
        file.close()
        
        id_alchs = []
        for i in range(0,len(file_lines)-9):
            if i % 8 == 0:
                temp_item_id = int(file_lines[i].strip()[1:].strip('": {'))
                value = int(file_lines[i+6].strip().strip('"value": '))
                high_alch = value * 0.6
                low_alch = value * 0.4        
                temp_item = [temp_item_id, high_alch, low_alch]
                id_alchs.append(temp_item)
    
    
        self._items= []
        for line in item_strings:
            if line != "":
                pairs = line.split(",")
                values = [i.split(":") for i in pairs]
                sell_average, name, overall_average, buy_average, sp, members, item_id = 0, 0, 0, 0, 0, 0, 0
                for k in range(0,len(values)):
                    attribute_tag = values[k][0].replace('"', "").replace("\'", "").strip()
                    if attribute_tag == "sell_average":
                        sell_average = int(values[k][1])
                    elif attribute_tag == 'name':
                        name = values[k][1].replace("\\", "").replace('"', "")
                    elif attribute_tag == "overall_average":
                        overall_average = int(values[k][1])
                    elif attribute_tag == "buy_average":
                        buy_average = int(values[k][1])
                    elif attribute_tag == "sp":
                        sp = int(values[k][1])
                    elif attribute_tag == "members":
                        members = values[k][1].strip()
                    elif attribute_tag == "id":
                        item_id = int(values[k][1])
                low_alch = 0
                high_alch = 0
                for item in id_alchs:
                    if item[0] == item_id:
                        low_alch = int(item[2])
                        high_alch = int(item[1])
                        break
                temp_item = Item(buy_average, sp, members, name, sell_average, overall_average, item_id, low_alch, high_alch)
                self._items.append(temp_item)

                
    def get_items(self):
        return self._items
        
    def print_profitable_bandit_sales(self, threshold, max_price):
        #prints all profitable items to buy from GE and sell to Bandit camps, with a profit threshold
        profitable_items = [] #name, price, high alch, profit margin
        for item in self.get_items():
                if item.get_ge_minus_high_alch() > threshold and item.get_high_alch() > 10 and item.get_buy_average() > 0 and item.get_members() == "true" and item.get_buy_average() < max_price:
                    temp_name = item.get_name() 
                    temp_sell_average = item.get_sell_average()
                    temp_high_alch = item.get_high_alch()
                    temp_profit_margin = item.get_ge_minus_high_alch()
                    profitable_items.append([temp_name, temp_sell_average, temp_high_alch, temp_profit_margin])
                      
        
        profitable_items = sorted(profitable_items, key = lambda x: x[3])
        line1 = 30
        line2 = 40
        line3 = 50
        line4 = 60
        print("")
        print("            name              | price |Hi_alch|profit")
        print("")
        for line in profitable_items:
            output_string = line[0]
            run = True
            counter = len(output_string)
            tag = 1
            while run:
                if tag == 4:
                    run = False                
                elif counter == 30 or counter == 35 or counter == 40:
                    output_string += "|  " + str(line[tag])
                    counter += len(str(line[tag]))
                    tag += 1
                
                else:
                    output_string += " "
                    counter += 1
            print(output_string)
        
        
        
INIT = Init()
threshold = int(input("Minimum profit margin per item threshold? "))
max_price = int(input("Maximum buy price? "))

INIT.print_profitable_bandit_sales(threshold, max_price)
end = input("")