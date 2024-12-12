import { useState } from "react";
import DatePicker from "react-datepicker";
import "react-datepicker/dist/react-datepicker.css";
import "./style.css";
const MyComponent = () => {
  const [selectedDate, setSelectedDate] = useState(null);
  // const selectOptions = ["Option 1", "Option 2", "Option 3"];

  return (
    <div>
      <DatePicker
        className='DataPicker'
        selected={selectedDate}
        onChange={(date) => setSelectedDate(date)}
        dateFormat='MM/dd/yyyy'
      />
      {/*
    <select id='Search'>
        {selectOptions.map((option, index) => (
          <option key={index} value={index}>
            {option}
          </option>
        ))}
      </select>
    */}
    </div>
  );
};

export default MyComponent;
