// 3 fetch requests for 3 endpints

(async () => {
	const petitions = [...Array(50000).keys()];

    const texts = await Promise.all(petitions.map(async el => {
        const resp = await fetch("http://localhost:8000/baW96F");
        console.log(el)
    }));

})();