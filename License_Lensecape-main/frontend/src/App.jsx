import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import Home from "./Home";
import VideoStrem from "./components/VideoStreaming/VideoStrem";
import Analytics from "./components/Analytics/Analytics";
import Activity from "./components/Activity/Activity";
import ListOfVe from "./components/ListOfVehicles/ListofVechiles";
import "./App.css";
// import SideBar from "./components/Sidebar/SideBar";
function App() {
  return (
    <Router>
      <Routes>
        <Route path='/' Component={Home} />
        <Route path='/VideoStrem' Component={VideoStrem} />
        <Route path='/Analytics' Component={Analytics} />
        <Route path='/ListOfVe' Component={ListOfVe} />
        <Route path='/Activity' Component={Activity} />
      </Routes>
    </Router>
  );
}

export default App;
