from langchain_openai import ChatOpenAI, OpenAI
from ...core.config import OPENAI_API_KEY, LARGE_LANGUAGE_MODEL
import imghdr
import base64

llm = ChatOpenAI(
    model=LARGE_LANGUAGE_MODEL,
    api_key=OPENAI_API_KEY,
    temperature=0,
)


def get_image_type(image_base64: str) -> str:
    image_bytes = base64.b64decode(image_base64)
    image_type = imghdr.what(None, h=image_bytes)
    ext = image_type if image_type else "png"  # default to png if type can't be determined
    return f"image/{ext}"


def describe_image(image_base64: str, context: str = "") -> str:
    prompt = (
        "You are analyzing an image extracted from a document.\n\n"
        "Provide:\n"
        "1. What type of image this is (photo, chart, diagram, screenshot, logo, etc.)\n"
        "2. All visible text, labels, numbers, and annotations\n"
        "3. If it's a chart/graph: the axes, data points, trends, and comparisons\n"
        "4. If it's a diagram/flowchart: the components, connections, and flow\n"
        "5. If it's a photo/screenshot: the key subjects and relevant details\n\n"
        "Be factual and thorough. Only describe what is visible in the image."
    )

    if context:
        prompt += f"\n\nDocument context: {context}"

    image_type = get_image_type(image_base64)
    response = llm.invoke([
        {
            "role": "user",
            "content": [
                {"type": "text", "text": prompt},
                {
                    "type": "image_url",
                    "image_url": {"url": f"data:{image_type};base64,{image_base64}"},
                },
            ],
        }
    ])
    return response.content


def summarize_table(table_content: str, table_html: str = None) -> str:
    table_data = table_html if table_html else table_content
    prompt = (
        "You are analyzing a table extracted from a document.\n\n"
        f"Table data:\n{table_data}\n\n"
        "Provide:\n"
        "1. What this table represents\n"
        "2. Column and row descriptions\n"
        "3. Key data points, trends, or comparisons\n"
        "4. Any notable outliers or patterns\n\n"
        "Be factual. Only describe what is in the table."
    )

    response = llm.invoke([{"role": "user", "content": prompt}])
    return response.content


def enrich_partitioned_document(partitioned: dict) -> dict:
    enriched_text_parts = [partitioned["text"]]

    for i, table in enumerate(partitioned["tables"]):
        summary = summarize_table(table["content"], table.get("html"))
        table["summary"] = summary
        enriched_text_parts.append(f"[Table {i + 1}, Page {table.get('page', '?')}]: {summary}")

    for i, image in enumerate(partitioned["images"]):
        if image.get("image_base64"):
            description = describe_image(image["image_base64"])
            image["description"] = description
            enriched_text_parts.append(f"[Image {i + 1}, Page {image.get('page', '?')}]: {description}")

    partitioned["enriched_text"] = "\n\n".join(enriched_text_parts)
    return partitioned
