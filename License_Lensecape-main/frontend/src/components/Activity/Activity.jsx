import "./style.css";
import { useState } from "react";
import GaugeChart from "./GaugeChart";
function Activity() {
  const [selectedItem, setSelectedItem] = useState("");

  const handleSelectionChange = (event) => {
    setSelectedItem(event.target.value);
  };
  const gaugeLabels = ["Label1", "Label2", "Label3"];
  return (
    <div className='Activity'>
      <div className='Activity-top'>
        <h2>Activity</h2>
        <select
          className='DropdownMenu'
          value={selectedItem}
          onChange={handleSelectionChange}>
          Selected item: {selectedItem}
          <option value=''>Week</option>
          <option value='Month'>Month</option>
          <option value='6-Months'>6-Months</option>
          <option value='1-Year'>1-Year</option>
        </select>
      </div>
      <div className='GaugeChart' id='0'>
        <GaugeChart
          labels={gaugeLabels}
          values={[55, 25, 20]}
          maxValue={100}
          // labels={["Label 1", "Label 2", "Label 3"]}
          cutoutPercentages={[10, 20, 30]}
          colors={["#FF6384", "#FFC3A0", "#f3f3f3"]}
        />
      </div>
    </div>
  );
}

export default Activity;
