import React, {Component } from 'react'
import axios from 'axios'

//Employee Component 
//State: Array with json data from http request
class EmployeesData extends Component{
    constructor(props) {
        super(props)

        this.state = {
            employees_data: []
        }
    }


    //ComponentDidMount() is a hook that gets invoked right after a React component 
    //has been mounted aka after the first render() lifecycle.
    //Allow us to update the component with new state when a promise resolves. 
    componentDidMount() {
        var host = process.env.REACT_APP_BACKEND;
        axios.get("http://" + host + ":10000/allrecords")
        .then(response => {
            console.log(response.data)
            this.setState({employees_data: response.data.response})
        })
        .catch(error => {
            console.log(error)
        })
    }
    
    //Reload page to mount component
    refresh(){
        window.location.reload();
    }
    
    render(){
        //Contain the array data from the json and is updated with the employeeData's state
        const{ employees_data} = this.state
        return (
            <header className="App-header">
            <button className="button-32" onClick={this.refresh}>Refresh</button>
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
                    <p className="name">{element.nombre}</p>
                    <p className="emotion">{element.emocion}</p>
                    <p className="date">{element.fecha}</p>
                </div>
                );
            })}
            </div>
        </header>
        )
    }
    

}

export default EmployeesData