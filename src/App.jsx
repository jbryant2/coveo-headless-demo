import { useEffect, useState } from 'react';
import { searchBox } from './controllers/searchBox';
import { resultList } from './controllers/resultList';

function App() {
  const [, forceUpdate] = useState(0);

  useEffect(() => {
    const unsub1 = searchBox.subscribe(() => forceUpdate(x => x + 1));
    const unsub2 = resultList.subscribe(() => forceUpdate(x => x + 1));

    return () => {
      unsub1();
      unsub2();
    };
  }, []);

  return (
    <div style={{ padding: '2rem' }}>
      <h1>Coveo Headless Search</h1>

      <input
        value={searchBox.state.value}
        onChange={(e) => searchBox.updateText(e.target.value)}
        onKeyDown={(e) => e.key === 'Enter' && searchBox.submit()}
        placeholder="Search..."
      />

      <div style={{ marginTop: '2rem' }}>
        {resultList.state.results.map(result => (
          <div key={result.uniqueId}>
            <h3>{result.title}</h3>
            <p>{result.excerpt}</p>
          </div>
        ))}
      </div>
    </div>
  );
}

export default App;
