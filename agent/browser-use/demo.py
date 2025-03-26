import io
import os
import asyncio
from dataclasses import dataclass
from typing import List, Optional
import logging

# Third-party imports
import gradio as gr
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
import numpy as np
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from pydantic import SecretStr

# Local module imports
from browser_use import Agent
from PIL import Image

from browser_use.browser.browser import Browser, BrowserConfig
from browser_use.browser.context import BrowserContext, BrowserContextConfig

load_dotenv()
logger = logging.getLogger(__name__)

@dataclass
class ActionResult:
	is_done: bool
	extracted_content: Optional[str]
	error: Optional[str]
	include_in_memory: bool


@dataclass
class AgentHistoryList:
	all_results: List[ActionResult]
	all_model_outputs: List[dict]

active_agents = {}
agent_lock = asyncio.Lock()

async def run_browser_task(
	task: str,
	base_url: str,
	api_key: str,
	model: str = '',
) :
	if not api_key.strip():
		return ("","Please provide an API key")
	try:
		with open("output.log", "r+") as f:  # 读写模式
			f.truncate(0)  # 将文件内容截断为0字节
	except FileNotFoundError:
		pass

	gifPath = task + '.gif'
	try:
			agent = Agent(
				task=task,
				llm=ChatOpenAI(model=model,base_url=base_url,api_key=SecretStr(api_key)),
				generate_gif=gifPath,
				browser=Browser(
					config=BrowserConfig(
						headless=True,  # This is True in production
						disable_security=True,
						new_context_config=BrowserContextConfig(
							no_viewport=True,
						)
					)
        		)
			)
			# Register agent with session ID
			async with agent_lock:
				active_agents[task] = agent
			
			result = await agent.run()
			return (result,result.final_result(),gifPath)

	except asyncio.CancelledError:
		# Handle cancellation for this session
		async with agent_lock:
			if task in active_agents:
				await active_agents[task].stop()
		return ("","Task cancelled by user")
	finally:
		# Cleanup agent registration
		async with agent_lock:
			if task in active_agents:
				del active_agents[task]

async def cancel_user_task(
	task: str,
) :
	"""Cancel task for specific user session"""
	try:
		async with agent_lock:
			if task in active_agents:
				await active_agents[task].stop()
				del active_agents[task]
				return ("","stop")
			return ("","No active task to cancel")
	finally:
		return ("","No active task to cancel")
	
async def capture_screenshots(
	task: str,
):
	"""Continuously capture screenshots during execution"""
	try:
		agent = active_agents[task]
		browserContext: BrowserContext = agent.browser_context	
		page = await browserContext.get_current_page()
		screenshot = await page.screenshot(
			timeout=1000,
			type='png',
			full_page=False,
			animations='disabled',
		)
		image = Image.open(io.BytesIO(screenshot))
		return image
	except Exception as e:
		return (f"failed{e}")
	finally:
		pass
	
async def read_log(task: str):
	try:
		if not os.path.exists("output.log"):
			return "⚠️ 文件不存在!"
		with open("output.log", "r") as f:				
			# 读取并解码内容
			content = f.read()
			# 分割行并获取最后50行
			lines = content.splitlines()[-30:]
			# 返回结果
			content = '\n'.join(lines)
			loginfo = f'```{content}```'
			return loginfo
	except Exception as e:
		return f"读取失败: {str(e)}"

async def read_file(task: str):
	while task in active_agents:
		await asyncio.sleep(3)
		log = await read_log(task)
		image = await capture_screenshots(task)
		yield log, image

def create_ui():
	with gr.Blocks(title='Browser Use GUI') as interface:
		gr.Markdown('# Browser Use Task Automation')

		with gr.Row():
			with gr.Column():
				with gr.Row():
					submit_btn = gr.Button('Run Task')
					preview_btn = gr.Button('Prewiew')
				log_info = gr.Markdown(label="📄 文件内容")
				base_url = gr.Textbox(label='Base URL', placeholder='https://...', type='text', value='http://xxx')
				api_key = gr.Textbox(label='OpenAI API Key', placeholder='sk-...', type='password', value='xxx')
				task = gr.Textbox(
					label='Task Description',
					placeholder='E.g., Find flights from New York to London for next week',
					lines=3,
					value='在腾讯新闻查询当前热点榜'
				)
				model = gr.Dropdown(
					choices=['gpt-4', 'deepseek-r1'], label='Model', value='deepseek-r1'
				)
			with gr.Column():
				stop_btn = gr.Button('Stop Running Task', variant='stop')
				image_output = gr.Image(label="Website Screenshot")
				gif = gr.Image(type="filepath", label="")
				history = gr.Textbox(label='History', lines=10, interactive=False)
				output = gr.Textbox(label='Output', lines=10, interactive=False)
				
		# Start task handler
		submit_btn.click(
			fn=lambda *args: asyncio.run(run_browser_task(*args)),
			inputs=[task, base_url, api_key, model],  # Session ID state
			outputs=[history, output, gif],
		)

		preview_btn.click(
			fn=read_file,
			inputs=[task], 
			outputs=[log_info, image_output],
		)

		stop_btn.click(
			fn=lambda *args: asyncio.run(cancel_user_task(*args)),
			inputs=[task], 
			outputs=[history, output],
		)

	return interface

if __name__ == '__main__':
	demo = create_ui()
	demo.launch(server_name="0.0.0.0", server_port=8082)