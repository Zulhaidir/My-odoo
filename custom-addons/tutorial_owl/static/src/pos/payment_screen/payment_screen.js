/** @odoo-module */

import PaymentScreen from "point_of_sale.PaymentScreen"
import Registries from "point_of_sale.Registries"

// const AExt1 = A => class extends A {}

const PaymentScreenInherit = (PaymentScreen) => class extends PaymentScreen {
    setup() {
        super.setup()
        console.log("Sudah ter-inherit ke Payment Screen")
    }

    addNewPaymentLine({ detail: paymentMethod }) {
        const payment_line = super.addNewPaymentLine({ detail: paymentMethod })
        console.log("Tambah payment line baru")
        return payment_line
    }

    go_next() {
        console.log("Anda meng-click next pada payment")
    }
}

Registries.Component.extend(PaymentScreen, PaymentScreenInherit)