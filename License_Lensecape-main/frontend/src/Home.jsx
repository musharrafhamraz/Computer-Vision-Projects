import SideBar from "./components/Sidebar/SideBar";
import Compo from "./components/Compo";

import "./App.css";
function Home() {
  return (
    <div className='Main'>
      <SideBar />
      <div>
        <Compo />
      </div>
    </div>
  );
}

export default Home;
