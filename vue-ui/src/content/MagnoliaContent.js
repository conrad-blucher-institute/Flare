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
  { href: "https://hohonu.io/", text: "Hohonu" },
  { href: "https://sherlock-prod.tamucc.edu/cbocp/magnolia-beach.html", text: "CBOCP Magnolia" },
]

// footer logos
export const footerLogos = [
  { href: "https://www.conradblucherinstitute.org/", src: "CBI-Logo.png", alt: "CBI Logo", class: "max-w-[165px] lg:max-w-[250px]"},
  { href: "https://www.coastaldynamicslab.org/", src: "CDL-Logo.png", alt: "Coastal Dynamics Lab Logo"}
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
		The dark blue line is for Hohonu, the green line is
		for base magnolia predictions, and the purple line
		is for magnolia transform predictions.
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
