import "./App.css";
import data from "./assets/data.json";
function App() {
  return (
    <div className="App">
      <header className="App-header">
        <h1>Employees Emotions</h1>
        <div className="header">
            <p className="name" >Name</p>
            <p className="emotion">Emotion</p>
            <p className="date">Date</p>
          </div>
        <div className="container">
          
          {data.response.map((element,index) => {
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
    </div>
  );
}

export default App;
