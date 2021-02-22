import { render } from 'react-dom';
import plotly from 'plotly.js';
import createPlotComponent from 'react-plotly.js/factory';
import { useEffect, useState } from 'react';
const Plot = createPlotComponent(plotly);

const App = () => {
  const [data, setData] = useState<any>();
  const [time, setTime] = useState<any>(0);

  useEffect(() => {
    let timer = setInterval(() => setTime((time: any) => time + 1), 1000);
    fetch('http://localhost:4000')
      .then((res: any) => res.json())
      .then((json) => setData(JSON.parse(json)))
      .finally(() => clearTimeout(timer));
  }, []);

  if (!data) return <>Loading ({time}s of ~30s)</>;

  return (
    <div style={{ display: 'grid', position: 'relative' }}>
      <Plot {...data} />
      <div
        style={{
          position: 'absolute',
          top: '1rem',
          left: '50%',
          transform: 'translateX(-50%)',
        }}
      >
        (Loaded in {time} seconds)
      </div>
    </div>
  );
};

render(<App />, document.getElementById('root'));
