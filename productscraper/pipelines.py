# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class ProductscraperPipeline:
    def process_item(self, item, spider):

        adapter = ItemAdapter(item)

        fieldNames = adapter.field_names()


        #strip whitespace from fields except description
        for field_name in fieldNames:
            if( field_name != 'description'):
                value = adapter.get(field_name)
                adapter[field_name] = value[0].strip()

        # Category and Product_type to lowercase
        lowercase_keys = ['category', 'product_type']

        for lowercase_key in lowercase_keys:
            value = adapter.get(lowercase_key)
            adapter[lowercase_key] = value.lower()
        
        # Extracting price and making float

        price_keys = ['price', 'price_excl_tax', 'price_incl_tax', 'tax']

        for price_key in price_keys:

            value = adapter.get(price_key)
            value = value.replace('£', '')
            adapter[price_key] = float(value)
        
        # extract availability number from string 
        avail_string = adapter.get('availability')

        split_string_array = avail_string.split('(')

        if len(split_string_array)< 2:
            adapter['availability'] = 0
        else:
            avail = split_string_array[1].split(' ')[0]
            adapter['availability'] = int(avail)

        
        # convert reviews to numbers

        num_reviews = adapter.get('num_reviews')
        adapter['num_reviews'] = int(num_reviews)

        # convert stars to number

        num_stars = adapter.get('stars')

        match num_stars :
            case 'five':
                adapter['stars'] = 5
            case  'four':
                adapter['stars'] = 4
            case 'three':
                adapter['stars'] = 3
            case 'two':
                adapter['stars'] = 2
            case 'one':
                adapter['stars'] = 1
            case _:
                adapter['stars'] = 0

        return item
