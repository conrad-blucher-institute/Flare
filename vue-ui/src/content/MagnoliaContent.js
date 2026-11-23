/*
	MagnoliaContent.js

	This script holds the static content for the magnolia page
	that is imported in the .vue file. Only static page content
	(no logic) should be placed in this file.

	Magnolia JS logic should go in useMagnolia.js and
	HTML logic should go in MagnoliaView.vue

	Created by: CJ Quintero
	Created on: 11/23/2026
*/

// footer links
export const footerLinks = [
  { href: "https://hohonu.io/", text: "Hohonu website" },
  { href: "https://sherlock-prod.tamucc.edu/cbocp/magnolia-beach.html", text: "Legacy CBOCP Magnolia Chart" },
]

// footer logos
export const footerLogos = [
  { href: "https://www.conradblucherinstitute.org/", src: "CBI-Logo.png", alt: "CBI Logo", class: "max-w-[165px] lg:max-w-[250px]"},
  { href: "https://www.coastaldynamicslab.org/", src: "CDL-Logo.png", alt: "Coastal Dynamics Lab Logo"},
  { href: "https://github.com/conrad-blucher-institute/semaphore", src: "Semaphore-Logo.png", alt: "Semaphore Logo"},
  { href: "https://www.nsf.gov/", src: "NSF-Logo.png", alt: "NSF Logo"},
  { href: "https://www.ai2es.org/", src: "ai2es-logo.png", alt: "AI2ES Logo" },
  { href: "https://hohonu.io/", src: "hohonu-logo.svg", alt: "Hohonu Logo"},
]

// graph sidebar info
export const graphInfo = {
	purpose: 
		`
		Shows recent <strong>Hohonu measurements</strong> alongside
		<strong>Semaphore Magnolia Predictions</strong> for Magnolia
		Beach TX.
		`,
	howToRead:
		`
		D2W measures the vertical distance from the sensor to the water surface.
		For example, a reading of 3 D2W feet indicates the water surface is 3 feet below the sensor.
		(A lower D2W number means a higher water level.)
		`,
	whatToLookFor:
		`
		Look for when the transform predictions cross the flooding
		threshold line.
		`,
	keepInMind:
		`
		This text is temporary and will be changed soon.
		`
}
