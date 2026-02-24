import PropTypes from 'prop-types';
import { Doughnut } from 'react-chartjs-2';
import { Chart as ChartJS, ArcElement, Tooltip, Legend } from 'chart.js';
import { useChart } from '../../hooks';

ChartJS.register(ArcElement, Tooltip, Legend);

const AllocationChart = ({ data = {} }) => {
  const { chartColors, getPieChartOptions } = useChart();

  const defaultData = {
    labels: ['AAPL', 'GOOGL', 'MSFT', 'AMZN', 'TSLA'],
    datasets: [
      {
        data: [25, 20, 20, 20, 15],
        backgroundColor: [
          chartColors.accent,
          chartColors.warning,
          '#00D4FF',
          '#FF6B9D',
          '#FFD700',
        ],
        borderColor: chartColors.primary,
        borderWidth: 2,
      },
    ],
  };

  return (
    <div className="w-full h-80 flex items-center justify-center">
      <Doughnut
        data={data.datasets ? data : defaultData}
        options={getPieChartOptions('Portfolio Allocation')}
      />
    </div>
  );
};

AllocationChart.propTypes = {
  data: PropTypes.object,
};

export default AllocationChart;
