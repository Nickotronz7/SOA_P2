import React, {Component } from 'react'
import axios from 'axios'
import data from '../assets/data.json'

class EmployeesData extends Component{
    constructor(props) {
        super(props)

        this.state = {
            employees_data: []
        }
    }



    componentDidMount() {
        axios.get('https://jsonplaceholder.typicode.com/posts')
        .then(response => {
            console.log(response)
            this.setState({employees_data: response.data})
        })
        .catch(error => {
            console.log(error)
        })
    }

    render(){
        const{ employees_data} = this.state
        return (
            <header className="App-header">
            <h1>Employees Emotions</h1>
            <div className="header">
                <p className="name" >Name</p>
                <p className="emotion">Emotion</p>
                <p className="date">Date</p>
            </div>
            <div className="container">
            
            
            {employees_data.map((element,index) => {
                return (
                <div key={index} className="tableLike">
                    <p className="name">{element.title}</p>
                    <p className="emotion">{element.body}</p>
                    <p className="date">{element.id}</p>
                </div>
                );
            })}
            </div>
        </header>
        )
    }
    

}

export default EmployeesData