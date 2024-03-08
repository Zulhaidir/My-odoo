/** @odoo-module */

import { PosGlobalState } from "point_of_sale.models"
import Registries from "point_of_sale.Registries"

const PosGlobalStateInherit = (models) => class extends models {
    constructor(obj) {
        super(obj);
        console.log("Sudah Bisa Inherited PosGlobalState")
        this.favorite_products = this.getFavoriteProducts()
    }

    async getFavoriteProducts(){
        const data = await this.env.services.rpc({
            'model': 'product.product',
            'method': 'getFavoriteProducts',
            'args': [{}]
        })
        
        return data
    }

}

Registries.Model.extend(PosGlobalState, PosGlobalStateInherit)