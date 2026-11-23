/*
	useMagnolia.js

	Composable file for MagnoliaView.vue. This file contains
	all the js code for MagnoliaView.vue. All HTML code
	should go in the vue file.

	Created by: CJ Quintero
	Created on: 11/23/2026
*/
import { ref, onMounted } from "vue"
import "highcharts/modules/exporting"
import "highcharts/modules/export-data"
import "highcharts/modules/offline-exporting"


// name of the file when downloading the csv
const BASE_FILENAME = "Magnolia_Water_Levels"
const csvURL = `${window.location.origin}/flare/csv-data/Magnolia.csv`


// colors of lines and text on the charts
const chartColors = {
	hohonu: 'blue',
	magnoliaTransform: 'purple',
	textColor: '#0f4f66',
}


const chartProps = (type) => ({
	/*
		chart properties

		Args:
			type (str) - The type of chart to create (line, bar, etc.)
		
		Returns:
			(object) - The common chart options for the specified chart type
	*/
  type,
  zoomType: "x",
  backgroundColor: "white",
  style: { fontFamily: "Arial" },
  marginRight: 30,
  marginTop: 100,
  events: fullscreenTooltipEvents,
})


const fullscreenTooltipEvents = {
	/* events to handle tooltip behavior when the chart is in fullscreen mode */
  fullscreenOpen: function () {
    this.update({ tooltip: { outside: false } });
  },
  fullscreenClose: function () {
    this.update({ tooltip: { outside: true } });
  },
};


const titleProps = (text) => ({
	/*
		title properties

		Args:
			text (str) - The text to display in the title
		
		Returns:
			(object) - The common title options with the specified title text
	*/
  text: text,
  style: {
    fontSize: "28px",
    fontWeight: "bold",
    color: chartColors.textColor,
  },
  useHTML: true,
  align: "center",
})


const exportingProps = {
	/* exporting properties */
  enabled: true,
  filename: `${BASE_FILENAME}`,
  sourceWidth: 1600,
  sourceHeight: 900,
  scale: 1,
  buttons: {
    contextButton: {
      menuItems: [
        "viewFullscreen",
        "separator",
        "downloadPNG",
        "downloadJPEG",
        "downloadPDF",
        "separator",
        "downloadCSV",
      ],
    },
  },
}


const legendProps = {
	/* legend properties */
  enabled: true,
  align: "center",
  verticalAlign: "bottom",
  layout: "horizontal",
  itemStyle: {
		color: chartColors.textColor,
		fontWeight: "normal",
		fontSize: "14px"
	},
}


const xAxisProps = {
	/* xAxis properties */
  type: "datetime",
  labels: {
    formatter: function () {
      const localDate = new Date(this.value)
      const day = localDate.toLocaleDateString("en-US", { weekday: "short" })
      const date = localDate.toLocaleDateString("en-US", { month: "short", day: "numeric" })
      return `<span style="display: block; text-align: center; font-family: Arial;"><b>${day}</b><br>${date}</span>`
    },
    useHTML: true,
    style: {
			fontSize: "16px",
			fontFamily: "Arial",
			color: chartColors.textColor,
			whiteSpace: "nowrap"
		},
  },
  title: {
    text: "Time",
    style: {
			fontSize: "20px",
			fontFamily: "Arial",
			color: chartColors.textColor,
		},
  },
	// Ensure ticks align to 12 AM
	tickPositioner: function () {
		const DAY = 24 * 3600 * 1000
		const positions = []
		const timezoneOffset = new Date().getTimezoneOffset() * 60 * 1000
		let tick = Math.floor((this.min - timezoneOffset) / DAY) * DAY + timezoneOffset

		// stop on the first tick past the last data point
		positions.push(tick)
		while (tick < this.max) {
			tick += 2 * DAY		// x axis ticks every 2 days
			positions.push(tick)
		}
		return positions
	},
	endOnTick: true,
}


const yAxisProps = {
	/* yAxis properties */
  labels: {
    style: {
			fontSize: "16px",
			color: chartColors.textColor,
			fontFamily: "Arial" 
		},
  },
  title: {
    text: "Height in feet (D2W)",
    style: {
			color: chartColors.textColor,
			fontSize: "20px"
		},
  },
  startOnTick: true,
  endOnTick: true,
	reversed: true,
	softMin: 3,
	softMax: 9,
}


const plotProps = {
	/* plot properties */
	series: {
		marker: {
			enabled: false,
			lineWidth: 1,
		},
		states: {
			inactive: { opacity: 1 }	// do not dim other series when hovering over one
		}
	},
	area: {
		states: {
			hover: {
				lineWidth: 4,
			}
		},
	}
}


const thresholdProps = {
	/* plotLines properties for the threshold line */
	value: 5,
	color: "red",
	dashStyle: "Dash",
	width: 2,
	zIndex: 4,	// draw above the series lines
	label: {
		text: "Approximate water level that can lead to flooding on nearby Ocean Drive.",
		align: "left",
		x: 10,
		y: -6,	// sit just above the line instead of on it
		style: {
			color: chartColors.textColor,
			fontSize: "14px",
			fontFamily: "Arial",
		},
	},
}


const tooltipProps = {
	/* tooltip properties */
	outside: true,
	shared: false,
	crosshairs: true,
	style: {
		fontSize: "14px",
		padding: "8px",
		color: chartColors.textColor,
		fontFamily: "Arial",
	},
	formatter: function () {
		return tooltipHeader(this.x) + `<b>${this.series.name}:</b> ${this.y.toFixed(1)} ft`
	},
}


const tooltipHeader = (x) => {
	/*
		tooltip options for all charts

		Args:
			x (int) - The current x value of the tooltip
		
		Returns:
			(str) - The formatted tooltip header with the date and time
	*/
  const localDate = new Date(x)
  const date = localDate.toLocaleDateString("en-US", {
		weekday: "long",
		month: "short",
		day: "numeric",
		year: "numeric",
	})
  const time = localDate.toLocaleTimeString("en-US", {
		hour: "2-digit",
		minute: "2-digit",
	})
  return `<b>Date: ${date}</b><br><b>Time: ${time}</b><br>`
}


const nowLineProps = () => {
	/* vertical line marking the current time, labeled with the date and time */
	const now = new Date()

	return {
		color: "red",
		width: 2,
		value: now.getTime(),
		dashStyle: "Solid",
		zIndex: 5,
		label: {
			text: 'Now',
			y: 20,
			style: {
				color: chartColors.textColor,
				fontSize: "14px",
				fontFamily: "Arial",
			},
		},
	}
}


const buildChart = (type, title) => ({
	/*
		builds a chart with the common options and returns it

		Args:
			type (str) - The type of chart to create (line, bar, etc.)
			title (str) - The title of the chart
	*/
	chart: chartProps(type),
	title: titleProps(title),
	exporting: exportingProps,
	legend: legendProps,
	xAxis: {
		...xAxisProps,
		plotLines: [nowLineProps()], // vertical now line
	},
	yAxis: {
		...yAxisProps,
		plotLines: [thresholdProps], // horizontal threshold line
	},
	plotOptions: plotProps,
	series: [],
	tooltip: tooltipProps,
})


const fetchData = async () => {
	/*
		fetches the CSV data from the specified URL and returns it as text

		Returns:
			(str) - The CSV data as text or null if there was an error
	*/

	try {
		const resp = await fetch(csvURL)
		if (!resp.ok) {
			throw new Error("Failed to fetch CSV data")
		}

		const csvText = await resp.text()
		return csvText
	} catch (error) {
		console.error("Error fetching CSV data:", error)
		return null
	}
}


const parseData = (csvText) => {
	/*
		parses the CSV data and returns it as an array of objects

		Args:
			csvText (str) - The CSV data as text
		
		Returns:
			(object) - An object with the parsed data for each series (hohonu, magnoliaTransform)
	*/

	const lines = csvText.trim().split(/\r?\n/);
  const header = lines[0].split(",");
  const col = (name) => header.indexOf(name);
	
	const data = {
		hohonu: [],
		magnoliaTransform: [],
	}

	// map the exact column name to the data key
	const keys = {
		hohonu: "hohonu_water_level_measurements",
		magnoliaTransform: "magnolia_transform_water_level_predictions",
	}

	lines.slice(1).forEach((line) => {
		const values = line.split(",")

		// timestamp is the first column (the df index), stored in UTC
		const [year, month, day, hour, minute, second] = values[0].split(/[- :]/).map(Number)
		const time = Date.UTC(year, month - 1, day, hour, minute, second || 0)
		if (isNaN(time)) {
			// skip this row if the timestamp is invalid
			return
		}

		// extract the columns and push the data to the corresponding arrays
		for (const [key, name] of Object.entries(keys)) {
      const raw = values[col(name)]
      if (raw && !isNaN(+raw)) {
				data[key].push([time, +raw])
			}
    }
	})

	return data
}


const convertToFeet = (data) => {
	/*
		converts the water level data from meters to feet

		NOTE: Hohonu is already in feet so only the magnolia predictions need to be converted

		Args:
			data (object) - An object with the parsed data for each series (hohonu, magnoliaTransform)
		
		Returns:
			(object) - An object with the converted data for each series (hohonu, magnoliaTransform)
	*/

	const toFeet = (meters) => meters * 3.28084
	const magnoliaTransform = data.magnoliaTransform.map(([time, value]) => [time, toFeet(value)])

	return {
		hohonu: data.hohonu,
		magnoliaTransform,
	}
}


const chartSeries = (data) => ([
	/*
		creates the series for the chart with the specified data

		Args:
			data (object) - An object with the parsed data for each series (hohonu, magnoliaTransform)
		
		Returns:
			(array) - An array of series objects for the chart
	*/
	{
		name: "Hohonu Water Level Measurements",
		type: "area",
		data: data.hohonu,
		color: chartColors.hohonu,			// the line itself
		fillColor: "rgba(15, 130, 245, 0.15)",	// light blue fill
		threshold: Infinity,				// fill toward the bottom of the chart
		lineWidth: 3,
		zIndex: 0,
	},
	{
		name: "Magnolia Transform Water Level Predictions",
		type: "line",
		data: data.magnoliaTransform,
		color: chartColors.magnoliaTransform,
		lineWidth: 3,
		zIndex: 1,
	}
])


export function useMagnolia() {
	/*
		main function that fetches, parses, and builds the charts
		for the magnolia page

		Returns:
			chartOptions - the magnolia chart options
			missingDataWarningBanner - the missing data banner that checks for missing
				data from chartOptions
	*/
	const chartOptions = ref({})
	const missingDataWarningBanner = ref(null)

	const loadCharts = async() => {
		// fetch, parse, and convert the data for the charts
		const csvText = await fetchData()
		if (!csvText) {
			console.error("No CSV data to load into charts")
			return
		}

		const parsedData = parseData(csvText)
		const data = convertToFeet(parsedData)

		// filter measurements to only be in the past
		// and predictions to only be in the future
		const now = Date.now()
		data.hohonu = data.hohonu.filter(([time]) => time <= now)
		data.magnoliaTransform = data.magnoliaTransform.filter(([time]) => time >= now)

		chartOptions.value = {
			...buildChart('line', 'Magnolia Water Level Predictions'),
			series: chartSeries(data),
		}
	}

	// load charts
	onMounted(async() => {
		await loadCharts()
		missingDataWarningBanner.value.checkForMissingDataAndWarn([chartOptions.value])
	})

	return { chartOptions, missingDataWarningBanner }
}
