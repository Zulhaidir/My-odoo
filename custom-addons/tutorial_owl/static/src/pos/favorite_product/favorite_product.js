/** @odoo-module */

import ProductScreen from "point_of_sale.ProductScreen"
import Registries from "point_of_sale.Registries"

const { onWillStart } = owl


const ProductScreenInherit = (ProductScreen) => class extends ProductScreen {
    setup() {
        super.setup()
        console.log("Sudah ter-inherit ke Product Screen")
        console.log("POS DB", this.env.pos.db)
        console.log("POS Services", this.env.services)

        this.favorite_products = []

        onWillStart(async () => {
            // const data = await this.env.services.rpc({
            //     'model': 'product.product',
            //     'method': 'search',
            //     'kwargs': {
            //         'domain': [['available_in_pos', '=', true], ['product_tag_ids', '=', 'Favorite']]
            //     }
            // })
            // this.favorite_products = data
            // console.log("RPC Data", data)

            // const data = await this.env.services.rpc({
            //     'model': 'product.product',
            //     'method': 'getFavoriteProducts',
            //     'args': [{}]
            // })

            // this.favorite_products = data
            
            this.favorite_products = await this.env.pos.favorite_products
            // console.log("RPC Data", data)
        })
    }

    get favoriteProducts() {
        // let products = this.env.pos.db.get_product_by_category(this.selectedCategoryId)

        let products = this.env.pos.db.product_by_id
        console.log("Product", products)
        let favorites = []
        this.favorite_products.forEach(i => favorites.push(products[i]))
        return favorites
    }
}

Registries.Component.extend(ProductScreen, ProductScreenInherit)