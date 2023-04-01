# This module is used to import any langchain class by name.

import importlib
from typing import Any

from langchain import PromptTemplate
from langchain.agents import Agent
from langchain.chains.base import Chain
from langchain.llms.base import BaseLLM
from langchain.tools import BaseTool

from langflow.interface.tools.util import get_tool_by_name


def import_module(module_path: str) -> Any:
    """Import module from module path"""
    if "from" not in module_path:
        # Import the module using the module path
        return importlib.import_module(module_path)
    # Split the module path into its components
    _, module_path, _, object_name = module_path.split()

    # Import the module using the module path
    module = importlib.import_module(module_path)

    return getattr(module, object_name)


def import_by_type(_type: str, name: str) -> Any:
    """Import class by type and name"""
    func_dict = {
        "agents": import_agent,
        "prompts": import_prompt,
        "llms": import_llm,
        "tools": import_tool,
        "chains": import_chain,
        "toolkits": import_toolkit,
        "wrappers": import_wrapper,
    }
    return func_dict[_type](name)


def import_class(class_path: str) -> Any:
    """Import class from class path"""
    module_path, class_name = class_path.rsplit(".", 1)
    module = import_module(module_path)
    return getattr(module, class_name)


def import_prompt(prompt: str) -> PromptTemplate:
    """Import prompt from prompt name"""
    if prompt == "ZeroShotPrompt":
        return import_class("langchain.prompts.PromptTemplate")
    return import_class(f"langchain.prompts.{prompt}")


def import_wrapper(wrapper: str) -> Any:
    """Import wrapper from wrapper name"""
    return import_module(f"from langchain.requests import {wrapper}")


def import_toolkit(toolkit: str) -> Any:
    """Import toolkit from toolkit name"""
    return import_module(f"from langchain.agents.agent_toolkits import {toolkit}")


def import_agent(agent: str) -> Agent:
    """Import agent from agent name"""
    # check for custom agent

    return import_class(f"langchain.agents.{agent}")


def import_llm(llm: str) -> BaseLLM:
    """Import llm from llm name"""
    return import_class(f"langchain.llms.{llm}")


def import_tool(tool: str) -> BaseTool:
    """Import tool from tool name"""

    return get_tool_by_name(tool)


def import_chain(chain: str) -> Chain:
    """Import chain from chain name"""
    return import_class(f"langchain.chains.{chain}")