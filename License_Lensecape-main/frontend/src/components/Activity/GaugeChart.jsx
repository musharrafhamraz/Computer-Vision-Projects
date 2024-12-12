import "chart.js/auto";
import { Doughnut } from "react-chartjs-2";
import PropTypes from "prop-types";

const GaugeChart = ({ values, labels, cutoutPercentages, colors }) => {
  const data = {
    labels: labels,
    datasets: [
      {
        data: values,
        backgroundColor: colors,
        hoverBackgroundColor: colors,
        cutout: cutoutPercentages,
      },
    ],
  };

  const options = {
    rotation: 270,
    circumference: 180,
    tooltips: { enabled: false },
    legend: { display: true },
    maintainAspectRatio: false,
  };

  return <Doughnut data={data} options={options} />;
};

GaugeChart.propTypes = {
  values: PropTypes.arrayOf(PropTypes.number).isRequired,
  maxValue: PropTypes.number.isRequired,
  labels: PropTypes.arrayOf(PropTypes.string).isRequired,
  cutoutPercentages: PropTypes.arrayOf(PropTypes.number).isRequired,
  colors: PropTypes.arrayOf(PropTypes.string).isRequired,
};

export default GaugeChart;
