"""
Outlook Integration — Windows-native Mail and Calendar access adapted from JARVIS.
"""

import datetime

def register(mcp):

    @mcp.tool()
    async def get_unread_emails(limit: int = 5) -> str:
        """
        Retrieves the latest unread emails from the user's local Windows Outlook application.
        Use this when the user asks "Do I have any emails?" or "Check my mail".
        """
        try:
            import win32com.client
            outlook = win32com.client.Dispatch("Outlook.Application").GetNamespace("MAPI")
            inbox = outlook.GetDefaultFolder(6) # 6 = Inbox
            
            # Filter for unread
            messages = inbox.Items
            messages.Sort("[ReceivedTime]", True) # Sort descending
            
            unread_msgs = []
            for msg in messages:
                if msg.UnRead:
                    unread_msgs.append(msg)
                if len(unread_msgs) >= limit:
                    break
            
            if not unread_msgs:
                return "You have no unread emails, sir."
                
            report = [f"You have {len(unread_msgs)} new emails, sir:"]
            for msg in unread_msgs:
                sender = getattr(msg, "SenderName", "Unknown")
                subject = getattr(msg, "Subject", "No Subject")
                report.append(f"- From {sender}: {subject}")
                
            return "\\n".join(report)
            
        except ImportError:
            return "The required 'pywin32' library is not installed."
        except Exception as e:
            return f"I'm unable to connect to Outlook, sir. It may not be configured properly. ({str(e)})"

    @mcp.tool()
    async def get_todays_calendar() -> str:
        """
        Retrieves today's calendar events from the user's local Windows Outlook application.
        Use this when the user asks "What's on my schedule?" or "Do I have any meetings?".
        """
        try:
            import win32com.client
            outlook = win32com.client.Dispatch("Outlook.Application").GetNamespace("MAPI")
            calendar = outlook.GetDefaultFolder(9) # 9 = Calendar
            
            today = datetime.date.today()
            tomorrow = today + datetime.timedelta(days=1)
            
            items = calendar.Items
            items.Sort("[Start]")
            items.IncludeRecurrences = True
            
            # Restrict to today
            restriction = f"[Start] >= '{today.strftime('%m/%d/%Y')} 12:00 AM' AND [Start] < '{tomorrow.strftime('%m/%d/%Y')} 12:00 AM'"
            restricted_items = items.Restrict(restriction)
            
            events = []
            for item in restricted_items:
                events.append(item)
                
            if not events:
                return "Your calendar is clear for today, sir."
                
            report = ["Here is your schedule for today:"]
            for event in events:
                subject = getattr(event, "Subject", "No Subject")
                start = getattr(event, "Start", None)
                if start:
                    # Format time as HH:MM AM/PM
                    time_str = start.strftime("%I:%M %p")
                    report.append(f"- {time_str}: {subject}")
                else:
                    report.append(f"- {subject}")
                    
            return "\\n".join(report)
            
        except Exception as e:
            return f"I couldn't access your calendar, sir. Outlook might not be running. ({str(e)})"
