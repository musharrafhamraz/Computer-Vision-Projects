import "./style.css";
import Bargraph from "./BarGrpah/Bargraph";
import { useState } from "react";

const TheAnalytics = () => {
  const [selectedItem, setSelectedItem] = useState("");

  const handleSelectionChange = (event) => {
    setSelectedItem(event.target.value);
  };
  return (
    <div className='TheAnalGraph'>
      <div className='Top-section'>
        <div>
          <h1>Analytics</h1>
        </div>
        <div className='TopMiddleSection'>
          <h2>
            <svg
              xmlns='http://www.w3.org/2000/svg'
              width='12'
              height='12'
              viewBox='0 0 12 12'
              fill='none'>
              <path
                d='M11.8574 5.98438C11.8574 9.14923 9.2918 11.7148 6.12695 11.7148C2.9621 11.7148 0.396484 9.14923 0.396484 5.98438C0.396484 2.81952 2.9621 0.253906 6.12695 0.253906C9.2918 0.253906 11.8574 2.81952 11.8574 5.98438Z'
                fill='#6359E9'
              />
            </svg>
            <span></span>
            Entry
          </h2>
          <h2>
            <svg
              xmlns='http://www.w3.org/2000/svg'
              width='13'
              height='12'
              viewBox='0 0 13 12'
              fill='none'>
              <path
                d='M12.2423 5.98438C12.2423 9.14923 9.67669 11.7148 6.51184 11.7148C3.34699 11.7148 0.781372 9.14923 0.781372 5.98438C0.781372 2.81952 3.34699 0.253906 6.51184 0.253906C9.67669 0.253906 12.2423 2.81952 12.2423 5.98438Z'
                fill='#64CFF6'
              />
            </svg>
            <span></span>
            Entry
          </h2>
          <div className='DropdownMenu'>
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
        </div>
      </div>
      <Bargraph selected={selectedItem} />
    </div>
  );
};

export default TheAnalytics;
