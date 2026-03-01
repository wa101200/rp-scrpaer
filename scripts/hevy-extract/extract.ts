import { createCLI, defineCommand, option } from "@bunli/core";
import { z } from "zod";

function extractSpec(jsSource: string): Record<string, unknown> {
	let captured: Record<string, unknown> | null = null;

	const window: Record<string, unknown> = {
		location: { search: "", origin: "" },
		ui: null,
		onload: null,
	};

	const SwaggerUIBundle = Object.assign(
		(opts: Record<string, unknown>) => {
			captured = (opts.spec ?? opts.swaggerDoc) as Record<string, unknown>;
			return {
				initOAuth() {},
				preauthorizeApiKey: () => true,
				authActions: { authorize() {} },
			};
		},
		{ presets: { apis: null }, plugins: { DownloadUrl: null } },
	);

	const SwaggerUIStandalonePreset = null;
	const setInterval = () => 0;

	// Evaluate the script — it assigns window.onload
	new Function(
		"window",
		"SwaggerUIBundle",
		"SwaggerUIStandalonePreset",
		"setInterval",
		jsSource,
	)(window, SwaggerUIBundle, SwaggerUIStandalonePreset, setInterval);

	// Call the onload handler the script registered
	if (typeof window.onload === "function") (window.onload as Function)();

	if (!captured) throw new Error("Failed to capture swaggerDoc from script");
	return captured;
}

const extract = defineCommand({
	name: "extract",
	description: "Extract the OpenAPI spec from Hevy API docs",
	options: {
		url: option(
			z.url().default("https://api.hevyapp.com/docs/swagger-ui-init.js"),
			{
				description: "URL of the swagger-ui-init.js file within hevy docs",
				short: "u",
			},
		),
		output: option(z.string().default("openapi.json"), {
			description: "Output file path",
			short: "o",
		}),
	},
	handler: async ({ flags, spinner }) => {
		const spin = spinner(`Fetching ${flags.url}`);
		spin.start();

		const jsSource = await fetch(flags.url).then((r) => r.text());
		const spec = extractSpec(jsSource);

		spin.update(`Writing to ${flags.output}`);
		await Bun.write(flags.output, JSON.stringify(spec, null, 2) + "\n");

		spin.succeed(
			`Written to ${flags.output} — ${Object.keys(spec.paths ?? {}).length} paths`,
		);
	},
});

(async () => {
	const cli = await createCLI({
		name: "hevy-extract",
		version: "0.1.0",
		description: "Extract OpenAPI spec from Hevy API docs",
	});

	cli.command(extract);
	await cli.run();
})();
