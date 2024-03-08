/** @odoo-module */

import { registry } from "@web/core/registry"
import { Layout } from "@web/search/layout"
import { getDefaultConfig } from "@web/views/view"
import { ConfirmationDialog } from "@web/core/confirmation_dialog/confirmation_dialog"
import { useService } from "@web/core/utils/hooks"
import { routeToUrl } from "@web/core/browser/router_service"
import { browser } from "@web/core/browser/browser"



const { Component, useSubEnv, useState } = owl

export class OwlOdooServices extends Component {
    setup() {
        console.log("sudah terhubung owl odoo services")
        this.display = {
            controlPanel: {"top-right": false, "bottom-right": false}
        }

        useSubEnv({
            config: {
                ...getDefaultConfig(),
                ...this.env.config,
            }
        })

        this.cookieService = useService("cookie")

        if (this.cookieService.current.dark_theme == undefined) {
            this.cookieService.setCookie("dark_theme", false)
        }

        const router = this.env.services.router

        this.state = useState({
            dark_theme: this.cookieService.current.dark_theme,
            get_http_data: [],
            post_http_data: [],
            rpc_data: [],
            orm_data: [],
            bg_success: router.current.search.bg_success,
            user_data: null,
            user_company: null,
        })

        const titleService = useService("title")
        titleService.setParts({zopenerp: "Zulhaidir", odoo: "sule", any: "bukanmain"})
        console.log(titleService.getParts())
    }

    showNotification() {
        const notification = this.env.services.notification
        notification.add("Ini adalah notiikasi sederhana", {
            title: "Odoo Notification Service",
            type: "info", //info, warning, danger, succuss
            sticky: true,
            className: "p-4",
            buttons: [
                {
                    name: "Notification Action",
                    onClick: () => {
                        console.log("Ini adalah action notification")
                    },
                    primary: true
                },
                {
                    name: "Show Me Again",
                    onClick: () => {
                        this.showNotification()
                    },
                    primary: false
                },
            ]
        })
    }

    showDialog() {
        const dialog = this.env.services.dialog
        dialog.add(ConfirmationDialog, {
            title: "Dialog Services",
            body: "Apakah anda yakin ingin melanjutkan action ini",
            confirm: () => {
                console.log("Dialog Terkonfirmasi")
            },
            cancel: () => {
                console.log("Dialog Dibatalkan")
            }
        },{
            onClose: () => {
                console.log("Dialog tertutup")
            }
        })
        console.log(dialog)
    }

    showEffect() {
        const effect = this.env.services.effect
        console.log(effect)
        effect.add({
            type: "rainbow_man",
            message: "Ini adalah effect odoo yang luar biasa"
        })
    }

    setCookeiService() {
        console.log("ini adalah cookie services")
        if (this.cookieService.current.dark_theme == 'false') {
            this.cookieService.setCookie("dark_theme", true)
        } else {
            this.cookieService.setCookie("dark_theme", false)
        }

        this.state.dark_theme = this.cookieService.current.dark_theme
        this.cookieService.deleteCookie("test")

    }

    async getHttpService() {
        const http = this.env.services.http
        console.log("Sudah bisa tersambung di http service")
        const data = await http.get("https://dummyjson.com/product")
        this.state.get_http_data = data.products
    }

    async postHttpService() {
        const http = this.env.services.http
        console.log("Sudah bisa tersambung di http service")
        const data = await http.post("https://dummyjson.com/products/add", {title: 'BMW Pencil'})
        console.log(data)
        this.state.post_http_data = data
    }

    async getRpcService() {
        const rpc = this.env.services.rpc
        // const data = await rpc('/owl/rpc_service')
        const data = await rpc('/owl/rpc_service', {limit: 15})
        console.log(data)
        this.state.rpc_data = data
    }

    async getOrmService() {
        const orm = this.env.services.orm
        const data = await orm.searchRead("res.partner", [], ['name', 'email'])
        console.log(data)
        this.state.orm_data = data
    }

    async getActionService() {
        const action = this.env.services.action
        console.log("sudah bisa terhubungn dengan Action Server")
        action.doAction({
            type: "ir.actions.act_window",
            name: "Action Service",
            res_model: "res.partner",
            domain: [],
            context: {search_default_type_company: 1},
            views: [
                [false, "list"],
                [false, "form"],
                [false, "kanban"],
            ],
            view_mode: "list, form, kanban",
            target: "current"
        })
    }

    getRouterService() {
        const router = this.env.services.router
        console.log("sudah bisa terhubung dengan Router Server")
        console.log(router)
        let { search } = router.current
        search.bg_success = search.bg_success == "1" ? "0" : "1"
        console.log(router.current)
        browser.location.href = browser.location.origin + routeToUrl(router.current)
    }

    getUserService() {
        const user = this.env.services.user
        console.log("sudah bisa tersambung di User Service")
        console.log(user)
        this.state.user_data = JSON.stringify(user)
    }

    getCompanyService() {
        const company = this.env.services.company
        console.log(company)
        this.state.user_company = JSON.stringify(company)
    }
}

OwlOdooServices.template = "tutorial_owl.OdooServices"
OwlOdooServices.components = { Layout }

registry.category('actions').add("odooServices", OwlOdooServices)