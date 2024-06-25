from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline

if __name__ == "__main__":
    # torch.cuda.empty_cache()
    tokenizer = AutoTokenizer.from_pretrained("ekshat/Llama-2-7b-chat-finetune-for-text2sql")

    # Loading model in 4 bit precision
    model = AutoModelForCausalLM.from_pretrained("ekshat/Llama-2-7b-chat-finetune-for-text2sql", load_in_4bit=True)

    context = "CREATE TABLE customers ( id int PRIMARY KEY, company varchar(50), last_name varchar(50), first_name varchar(50), email_address varchar(50), address varchar(50), city varchar(50) ); CREATE TABLE employees ( id int PRIMARY KEY, company varchar(50), last_name varchar(50), first_name varchar(50), email_address varchar(50), address varchar(50), city varchar(50) ); CREATE TABLE order_details ( id int PRIMARY KEY, order_id int, product_id int  , quantity decimal(18,4), unit_price decimal(19,4), discount double, status_id int, date_allocated datetime, purchase_order_id int, inventory_id int ); CREATE TABLE order_details_status ( id int PRIMARY KEY, status_name varchar(50) ); CREATE TABLE orders ( id int PRIMARY KEY, employee_id int, customer_id int, order_date datetime, shipped_date datetime, shipper_id int, ship_name varchar(50), ship_address varchar(50), ship_city varchar(50), shipping_fee decimal(19,4), taxes decimal(19,4), payment_type varchar(50), paid_date datetime, tax_rate double, status_id int ); CREATE TABLE orders_status ( id int PRIMARY KEY, status_name varchar(50), ); CREATE TABLE products ( supplier_ids varchar(50), id int PRIMARY KEY, product_code varchar(25), product_name varchar(50), description varchar(50), standard_cost decimal(19,4), list_price decimal(19,4), reorder_level int, target_level int, quantity_per_unit varchar(50), discontinued int, minimum_reorder_quantity int, category varchar(50) ); CREATE TABLE shippers ( id int PRIMARY KEY, company varchar(50), last_name varchar(50), first_name varchar(50), email_address varchar(50), address varchar(50), city varchar(50) ); CREATE TABLE suppliers ( id int PRIMARY KEY, company varchar(50), last_name varchar(50), first_name varchar(50), email_address varchar(50), address varchar(50), city varchar(50) ); -- orders.customer_id can be joined with customers.id -- orders.employee_id can be joined with employees.id -- orders.status_id can be joined with orders_status.id -- orders.shipper_id can be joined with shippers.id -- order_details.order_id can be joined with orders.id -- order_details.status_id can be joined with order_details_status.id -- order_details.product_id can be joined with products.id"

    question = "What are the most popular ordered products"
    # question = "How much discount from orders with a product_code of NWTB-1 did I make last month"

    prompt = f"""Below is a context that describes a sql query, paired with a question that provides further information. Write an answer that appropriately completes the request.
    ### Context:
    {context}
    ### Question:
    {question}
    ### Answer:"""

    pipe = pipeline(task="text-generation", model=model, tokenizer=tokenizer, max_new_tokens=300)
    result = pipe(prompt)
    print(result[0]['generated_text'])
