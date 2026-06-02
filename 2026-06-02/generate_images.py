import anthropic
import base64
import os
import time

client = anthropic.Anthropic(
    api_key="sk-YNZXuLFxZz00vf0AHb4mE3HXdWdiICOJLsisAepsRvCPTYU7",
    base_url="https://www.yaoxinapi.com"
)

prompts = [
    "NVIDIA factory floor with robotic arms, AI monitoring screens showing real-time production data, futuristic smart manufacturing facility, industrial AI dashboard, photorealistic, high-tech atmosphere",
    "Samsung smart factory interior, Korean SME workers collaborating with AI systems, modern production line with IoT sensors, automated quality control, professional industrial photography",
    "Advanced nanotechnology lab with AI-powered microscopes, semiconductor manufacturing equipment, diverse workers learning with AR/VR headsets, skills training environment, educational technology",
    "Taboola Realize+ agentic AI marketing platform interface, autonomous ad optimization dashboard, third-generation marketing automation, modern SaaS product screenshot style, clean UI design",
    "OuterSignal Monocle AI personalization platform, customer intelligence graphs, lifecycle marketing automation interface, e-commerce dashboard with real-time personalization analytics",
    "Google AI Max advertising interface, dynamic creative generation in action, automated search ads platform, Google Ads UI redesign, modern advertising technology, clean product design",
    "ESMFold2 protein structure visualization, 3D molecular models floating in space, AlphaFold comparison charts, computational biology lab with advanced screens, scientific breakthrough atmosphere",
    "Isomorphic Labs AI drug discovery facility, futuristic pharmaceutical research lab, AlphaFold-powered drug design screens, scientists working with AI systems, biotech innovation",
    "Biohub ESM protein language model visualization, therapeutic discovery platform interface, protein function mapping dashboard, modern biology research facility, cutting-edge science",
    "Claude Opus 4.8 dynamic workflow visualization, hundreds of parallel AI agents working together, Claude Code interface with workflow orchestration, modern AI development environment",
    "NVIDIA Cosmos 3 physical AI simulation, robotic training environment with mixture-of-transformers architecture, open-source AI model visualization, industrial robotics lab",
    "SpaceX Grok AI coding interface, massive 1.5 trillion parameter model visualization, advanced code generation system, futuristic AI development platform, Elon Musk vision",
    "Enterprise agentic AI control plane, Microsoft Salesforce ServiceNow logos integrated, autonomous business process automation, corporate AI operations center, professional business technology",
    "CoreWeave unified agentic AI deployment platform, continuous autonomous improvement visualization, production AI agent monitoring dashboard, cloud infrastructure with AI orchestration",
    "AWS AgentCore payment system architecture diagram, billions of AI agents transacting autonomously, agentic commerce infrastructure, distributed ledger visualization, enterprise fintech"
]

output_dir = "/home/mayuzhou/ai_news/2026-06-02/images"
os.makedirs(output_dir, exist_ok=True)

for i, prompt in enumerate(prompts, 1):
    card_num = f"{i:02d}"
    output_path = f"{output_dir}/card-{card_num}.jpg"

    if os.path.exists(output_path):
        print(f"SKIP: card-{card_num} (already exists)")
        continue

    print(f"GEN: card-{card_num}...")

    max_retries = 3
    for attempt in range(max_retries):
        try:
            message = client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=1024,
                messages=[{
                    "role": "user",
                    "content": f"Generate an image: {prompt}"
                }]
            )

            image_block = next(
                (block for block in message.content if block.type == "image"),
                None
            )

            if image_block:
                image_data = base64.b64decode(image_block.source.data)
                with open(output_path, "wb") as f:
                    f.write(image_data)

                size_kb = len(image_data) / 1024
                print(f"OK: card-{card_num} ({size_kb:.0f}KB)")
                time.sleep(1)
                break
            else:
                print(f"  [{attempt+1}] FAIL: No image in response")
                if attempt < max_retries - 1:
                    time.sleep(2)

        except Exception as e:
            print(f"  [{attempt+1}] FAIL: {e}")
            if attempt < max_retries - 1:
                time.sleep(2)
    else:
        print(f"SKIP: card-{card_num} (max retries reached)")

print("\nDONE: All images processed")
