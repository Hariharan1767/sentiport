import PropTypes from 'prop-types';
import { Line } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
} from 'chart.js';
import { useChart } from '../../hooks';

ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend);

const PerformanceChart = ({ data = {} }) => {
  const { chartColors, getLineChartOptions } = useChart();

  const defaultData = {
    labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
    datasets: [
      {
        label: 'Sentiment Portfolio',
        data: [12, 19, 3, 5, 2, 3],
        borderColor: chartColors.accent,
        backgroundColor: `rgba(0, 255, 136, 0.1)`,
        tension: 0.4,
      },
      {
        label: 'Traditional Portfolio',
        data: [8, 15, 2, 4, 1, 2],
        borderColor: chartColors.warning,
        backgroundColor: `rgba(255, 184, 0, 0.1)`,
        tension: 0.4,
      },
      {
        label: 'Benchmark',
        data: [5, 10, 1, 3, 0, 1],
        borderColor: chartColors.secondary,
        backgroundColor: `rgba(26, 31, 58, 0.1)`,
        tension: 0.4,
      },
    ],
  };

  return (
    <div className="w-full h-80">
      <Line data={data.datasets ? data : defaultData} options={getLineChartOptions('Portfolio Performance')} />
    </div>
  );
};

PerformanceChart.propTypes = {
  data: PropTypes.object,
};

export default PerformanceChart;
