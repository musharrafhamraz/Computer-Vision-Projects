import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
} from "recharts";

const data = [
  { name: "Jan", Exit: 4000, Entry: 2400, amt: 2400 },
  { name: "Feb", Exit: 3000, Entry: 1398, amt: 2210 },
  { name: "Mar", Exit: 2000, Entry: 9800, amt: 2290 },
  { name: "Apr", Exit: 2780, Entry: 3908, amt: 2000 },
  { name: "May", Exit: 1890, Entry: 4800, amt: 2181 },
  { name: "Jun", Exit: 2390, Entry: 3800, amt: 2500 },
  { name: "Jul", Exit: 3490, Entry: 4300, amt: 2100 },
];

const BarGraph = ({ selected }) => {
  let graphContent;
  switch (selected) {
    case "Month":
      graphContent = "Displaying data for the selected Month";
      break;
    case "6-Months":
      graphContent = "Displaying data for the selected 6-Months";
      break;
    case "1-Year":
      graphContent = "Displaying data for the selected 1-Year";
      break;
    default:
      graphContent =
        "Displaying default data (e.g., data for the selected Week)";
      break;
  }

  return (
    <div className='Bargraph'>
      <p>{graphContent}</p>
      <BarChart width={600} height={300} data={data}>
        <CartesianGrid strokeDasharray='3 0' />
        <XAxis dataKey='name' />
        <YAxis />
        <Tooltip />
        <Legend />
        <Bar dataKey='Exit' fill='#64CFF6' />
        <Bar dataKey='Entry' fill='#6359E9' />
      </BarChart>
    </div>
  );
};

export default BarGraph;
