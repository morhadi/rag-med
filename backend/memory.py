"""
Conversation memory management using LangChain
Single persistent memory instance for the entire session
"""
from langchain.memory import ConversationBufferMemory
import logging

logger = logging.getLogger(__name__)

# Global memory instance - persists throughout app lifetime
_global_memory = None

def get_memory() -> ConversationBufferMemory:
    """
    Get or create the global conversation memory instance
    
    Returns:
        ConversationBufferMemory: Persistent memory for the session
    """
    global _global_memory
    
    if _global_memory is None:
        logger.info("Initializing new conversation memory")
        _global_memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True,
            output_key="answer",
            input_key="question"
        )
    
    return _global_memory

def clear_memory():
    """
    Clear the conversation memory
    Useful for starting a fresh conversation
    """
    global _global_memory
    
    if _global_memory is not None:
        _global_memory.clear()
        logger.info("Conversation memory cleared")
    else:
        logger.warning("Attempted to clear memory but no memory instance exists")

def get_conversation_history() -> list:
    """
    Get the full conversation history
    
    Returns:
        list: List of message objects from the conversation
    """
    memory = get_memory()
    return memory.chat_memory.messages

def add_to_memory(question: str, answer: str):
    """
    Manually add a Q&A pair to memory
    
    Args:
        question: User's question
        answer: Assistant's answer
    """
    memory = get_memory()
    memory.save_context(
        {"question": question},
        {"answer": answer}
    )
    logger.debug(f"Added to memory - Q: {question[:50]}... A: {answer[:50]}...")
