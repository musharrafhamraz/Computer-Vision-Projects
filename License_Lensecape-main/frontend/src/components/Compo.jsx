import "./style.css";
import Searchbar from "./searchbar/Seacrhbar";
import VideoStrem from "./VideoStreaming/VideoStrem";
import Activity from "./Activity/Activity";
import Analytics from "./Analytics/Analytics";
import AnalyticGraph from "./TheAnalyticgraph/TheAnalytics";
import ListofVechiles from "./ListOfVehicles/ListofVechiles";

function Compo() {
  return (
    <div className='Compo'>
      <Searchbar />
      <div className='Compo-section-two'>
        <div className='vid-Analy'>
          <VideoStrem />
          <AnalyticGraph />
        </div>
        <div className='Activ-Analy'>
          <Activity />
          <Analytics />
        </div>
      </div>
      <ListofVechiles />
    </div>
  );
}

export default Compo;
