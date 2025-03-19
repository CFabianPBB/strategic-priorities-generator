import os
import json
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv()

# Get OpenAI API key from environment
openai_api_key = os.getenv("OPENAI_API_KEY")

# Initialize the OpenAI client
client = OpenAI(api_key=openai_api_key)

def generate_strategic_priorities(org_name: str, org_website: str):
    """
    Generate strategic priorities for an organization using OpenAI.
    
    Args:
        org_name: Name of the organization
        org_website: Website of the organization
        
    Returns:
        A list of priority dictionaries with 'priority', 'description', and 'definitions'
    """
    try:
        # Validate API key
        if not openai_api_key:
            print("Warning: OpenAI API key not found in environment variables")
            return None
            
        # Create the prompt
        prompt = f"""
        Please identify EXACTLY 5-7 strategic priorities for {org_name} that define why they exist, that they can use for Priority Based Budgeting. And for each priority, please also identify EXACTLY 5-7 result definitions that describe how the priority is achieved. One of the priorities MUST be GOVERNANCE or HIGH PERFORMING GOVERNMENT.
        
        Please consider:
        1. Use information from {org_website} and any current strategic plans you know about.
        2. Include both community-oriented priorities, as well as internal governance priorities.
        3. Be descriptive and detailed in your explanations.
        
        Each priority should include:
        - A clear title
        - A description explaining why this priority exists
        - 5-7 result definitions with clear titles and descriptions
        
        The output should follow this JSON structure precisely:
        [
          {
            "priority": "Priority Title",
            "description": "Description of the priority",
            "definitions": [
              {
                "title": "Result Definition Title",
                "description": "Description of how this result is achieved"
              },
              ...more definitions...
            ]
          },
          ...more priorities...
        ]
        
        Return ONLY the JSON structure with no additional explanation.
        """
        
        # Call OpenAI API
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=5000
        )
        
        # Extract content from response
        content = response.choices[0].message.content.strip()
        
        # Parse the JSON content
        try:
            # Find the start and end of the JSON structure
            json_start = content.find('[')
            json_end = content.rfind(']') + 1
            
            if json_start >= 0 and json_end > json_start:
                json_content = content[json_start:json_end]
                priorities = json.loads(json_content)
                return priorities
            else:
                # If we can't find valid JSON brackets, try parsing the whole response
                priorities = json.loads(content)
                return priorities
                
        except json.JSONDecodeError as e:
            print(f"Error parsing JSON from OpenAI response: {e}")
            print(f"Response content: {content}")
            
            # Attempt to clean and fix common JSON formatting issues
            try:
                # Replace single quotes with double quotes
                content_fixed = content.replace("'", "\"")
                priorities = json.loads(content_fixed)
                return priorities
            except:
                # If all parsing attempts fail, return None
                print("All JSON parsing attempts failed")
                return None
                
    except Exception as e:
        print(f"Error generating priorities with OpenAI: {e}")
        return None

# Fallback function for when OpenAI is not available
def generate_mock_priorities(org_name: str):
    """Generate mock strategic priorities when OpenAI is not available."""
    priorities = [
        {
            "priority": "Safe and Secure Communities",
            "description": f"Ensuring public safety and justice for all residents of {org_name} by protecting communities from crime and harm while upholding fairness and accountability in the justice system.",
            "definitions": [
                {
                    "title": "Effective & Equitable Law Enforcement:",
                    "description": "Prevent crime and respond quickly to emergencies through community-oriented policing and accountable practices that build public trust."
                },
                {
                    "title": "Justice Reform & Alternatives to Incarceration:",
                    "description": "Implement diversion programs and treatment services (embodying the \"Care First, Jails Last\" approach) so social and mental health issues are addressed with health interventions instead of jail whenever possible."
                },
                {
                    "title": "Fire and Emergency Medical Services:",
                    "description": "Provide effective fire protection and emergency medical response across all communities, ensuring well-coordinated responses to fires, accidents, and medical emergencies to safeguard lives and property."
                },
                {
                    "title": "Emergency Preparedness & Disaster Response:",
                    "description": "Maintain robust preparedness plans and rapid-response protocols for natural disasters, public health crises, and other emergencies, coordinating law enforcement, fire, and health agencies to protect the public."
                },
                {
                    "title": "Protecting Vulnerable Populations:",
                    "description": "Collaborate across agencies to prevent abuse, neglect, and exploitation, focusing on at-risk children, seniors, and other vulnerable groups through early intervention and supportive services."
                },
                {
                    "title": "Transparency & Oversight:",
                    "description": "Ensure accountability in all public safety agencies by strengthening oversight, increasing transparency, and engaging the community in oversight processes - fostering integrity and trust in law enforcement and the justice system."
                }
            ]
        },
        {
            "priority": "Economic Development & Job Creation",
            "description": f"Strengthen {org_name}'s economy by supporting business growth, attracting investment, and creating quality jobs that provide pathways to prosperity for all residents.",
            "definitions": [
                {
                    "title": "Business Growth & Support:",
                    "description": "Facilitate the creation and expansion of local businesses through streamlined permitting, technical assistance, and access to capital, with particular focus on small and minority-owned enterprises."
                },
                {
                    "title": "Workforce Development:",
                    "description": "Partner with educational institutions and industries to provide job training, skill development, and career pathways that prepare residents for quality jobs in growing sectors."
                },
                {
                    "title": "Strategic Investment:",
                    "description": "Target public investments to catalyze private development in key geographic areas and industry sectors, creating jobs and strengthening the tax base."
                },
                {
                    "title": "Inclusive Economic Growth:",
                    "description": "Ensure economic development benefits all communities by focusing on underserved areas and reducing barriers to participation in the economy."
                },
                {
                    "title": "Innovation & Technology:",
                    "description": "Foster innovation, research, and technology development to position the region as a leader in emerging industries and the knowledge economy."
                }
            ]
        },
        {
            "priority": "Infrastructure & Sustainable Development",
            "description": f"Develop and maintain {org_name}'s physical infrastructure to support quality of life, economic vitality, and environmental sustainability.",
            "definitions": [
                {
                    "title": "Transportation Networks:",
                    "description": "Develop and maintain a comprehensive, multimodal transportation system that safely and efficiently moves people and goods while reducing congestion and environmental impacts."
                },
                {
                    "title": "Sustainable Environmental Practices:",
                    "description": "Implement policies and programs that conserve natural resources, reduce pollution, and build resilience to climate change impacts."
                },
                {
                    "title": "Smart Growth & Planning:",
                    "description": "Guide development to create livable, walkable communities that balance housing, jobs, and services while preserving open space and community character."
                },
                {
                    "title": "Water Management:",
                    "description": "Ensure reliable, sustainable water supplies through conservation, storage, recycling, and protection of water quality."
                },
                {
                    "title": "Public Facilities:",
                    "description": "Build and maintain high-quality public facilities that serve community needs, enhance quality of life, and demonstrate environmental leadership."
                }
            ]
        }
    ]
    return priorities