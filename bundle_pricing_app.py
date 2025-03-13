import streamlit as st
import pandas as pd

def calculate_bundle_price(products, discount):
    total_cost = sum(p["purchase_price"] * p["quantity"] for p in products)
    total_sale_price = sum(p["sale_price"] * p["quantity"] for p in products)
    bundle_price = total_sale_price * (1 - discount / 100)
    net_margin = bundle_price - total_cost
    return total_cost, total_sale_price, bundle_price, net_margin

# Streamlit App
st.title("BundleDG Calculator")

# Session state for storing products
if "products" not in st.session_state:
    st.session_state.products = []

# Input fields for product details
with st.form("add_product"):
    sku = st.text_input("Product SKU")
    quantity = st.number_input("Quantity", min_value=1, step=1, format="%d")
    purchase_price = st.number_input("Purchase Price (€)", min_value=0.0, format="%.2f")
    sale_price = st.number_input("Sale Price (€)", min_value=0.0, format="%.2f")
    add_product = st.form_submit_button("Add Product")
    
    if add_product and sku:
        st.session_state.products.append({
            "sku": sku,
            "quantity": quantity,
            "purchase_price": purchase_price,
            "sale_price": sale_price
        })

# Display added products
if st.session_state.products:
    st.subheader("Products in Bundle")
    df = pd.DataFrame(st.session_state.products)
    st.dataframe(df)
    
    # Discount input
    discount = st.slider("Discount on Bundle (%)", min_value=0, max_value=100, value=20)
    
    # Calculate button
    if st.button("Calcola"):
        # Calculate prices
        total_cost, total_sale_price, bundle_price, net_margin = calculate_bundle_price(st.session_state.products, discount)
        
        # Display results
        st.subheader("Bundle Summary")
        st.write(f"**Total Purchase Cost:** €{total_cost:.2f}")
        st.write(f"**Total Sale Price:** €{total_sale_price:.2f}")
        st.write(f"**Bundle Price after Discount:** €{bundle_price:.2f}")
        st.write(f"**Net Margin:** €{net_margin:.2f}")
        
        # Export to Excel
        if st.button("Export to Excel"):
            bundle_df = pd.DataFrame([{
                "Total Purchase Cost (€)": total_cost,
                "Total Sale Price (€)": total_sale_price,
                "Discount Applied (%)": discount,
                "Bundle Price (€)": bundle_price,
                "Net Margin (€)": net_margin
            }])
            
            excel_path = "bundle_pricing.xlsx"
            bundle_df.to_excel(excel_path, index=False)
            st.download_button(label="Download Excel", data=open(excel_path, "rb"), file_name="bundle_pricing.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
