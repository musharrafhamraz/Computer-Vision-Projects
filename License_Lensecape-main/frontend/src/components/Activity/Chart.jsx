// import { useEffect } from "react";
// import Chart from "react-apexcharts";

// const MyChartComponent = () => {
//   const options = {
//     series: [76],
//     chart: {
//       type: "radialBar",
//       offsetY: -20,
//       sparkline: {
//         enabled: true,
//       },
//     },
//     plotOptions: {
//       radialBar: {
//         startAngle: -90,
//         endAngle: 90,
//         track: {
//           background: "#e7e7e7",
//           strokeWidth: "97%",
//           margin: 5,
//           dropShadow: {
//             enabled: true,
//             top: 2,
//             left: 0,
//             color: "#999",
//             opacity: 1,
//             blur: 2,
//           },
//         },
//         dataLabels: {
//           name: {
//             show: false,
//           },
//           value: {
//             offsetY: -2,
//             fontSize: "22px",
//           },
//         },
//       },
//     },
//     grid: {
//       padding: {
//         top: -10,
//       },
//     },
//     fill: {
//       type: "gradient",
//       gradient: {
//         shade: "light",
//         shadeIntensity: 0.4,
//         inverseColors: false,
//         opacityFrom: 1,
//         opacityTo: 1,
//         stops: [0, 50, 53, 91],
//       },
//     },
//     labels: ["Average Results"],
//   };

//   useEffect(() => {
//     const chart = new ApexCharts(document.querySelector("#chart"), options);
//     chart.render();

//     // Cleanup function to destroy the chart when the component unmounts
//     return () => {
//       chart.destroy();
//     };
//   }, []); // Empty dependency array to run the effect only once

//   return <div id='chart'>{/* Chart will be rendered here */}</div>;
// };

// export default MyChartComponent;
