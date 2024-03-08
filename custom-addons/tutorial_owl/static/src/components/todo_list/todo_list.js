/** @odoo-module **/

import { registry } from '@web/core/registry';
const { Component, useState, onWillStart, useRef } = owl;

//untuk mendapatkan data dari database bersama dengan onWillStart
import { useService } from "@web/core/utils/hooks";             

export class OwlTodoList extends Component {
    setup() {

        this.state = useState({
            task:{name: "", color:"#ffa500", completed: false},
            taskList:[],
            isEdit: false,
            activeId: false,
        })
        console.log(this.state)

        this.orm = useService("orm")
        this.model = "owl.todo.list"
        this.searchInput = useRef("search-input")

        onWillStart(async () => {
            await this.getAllTasks()
        })
    }

    //tampilkan semua task
    async getAllTasks() {
        this.state.taskList = await this.orm.searchRead(this.model, [], ["name", "color", "completed"])
    }

    //new
    async addTask() {
        await this.resetForm()
        this.state.activeId = false
        this.state.isEdit = false
    }
    async resetForm() {
        this.state.task = {name: "", color:"#ffa500", completed: false}
    }

    //edit
    async editTask(task) {
        this.state.activeId = await task.id
        this.state.isEdit = true
        this.state.task = await {...task}    //{name: task.name, color: task.color, completed: task.completed}
    }

    //delete
    async deleteTask(task) {
        await this.orm.unlink(this.model, [task.id]) 
        await this.getAllTasks()
    }

    //save
    async saveTask() {
        if (!this.state.isEdit) {
            await this.orm.create(this.model, [this.state.task])            
        } else {
            await this.orm.write(this.model, [this.state.activeId], this.state.task)            
        }
        await this.getAllTasks()
    }

    //search
    async searchTasks() {
        const text = this.searchInput.el.value
        this.state.taskList = await this.orm.searchRead(this.model, [['name', 'ilike', text]], ["name", "color", "completed"])
    }

    //udpate checkbox di task list
    async toogleTask(e, task) {
        await this.orm.write(this.model, [task.id], {completed: e.target.checked})
        await this.getAllTasks()
    }

    //update color di task list
    async updateColor(e, task) {
        await this.orm.write(this.model, [task.id], {color: e.target.value})
        await this.getAllTasks()
    }
}

OwlTodoList.template = 'owl.TodoList'

registry.category('actions').add('tutorial_owl.action_todo_list_js', OwlTodoList);
