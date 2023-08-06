import pandas as pd
from gql import gql, Client#, AIOHTTPTransport, RequestsHTTPTransport # This is gql version 3
from gql.transport.requests import RequestsHTTPTransport
from loguru import logger

from .utils.ut_programming import ProgrammingUtils
from .utils.ut_core import Utils

class Programming():

    def __init__(self, accessToken:str, endpoint:str) -> None:
    
        #endpoint = 'http://172.16.2.206:8140/graphql/'
        
        header = {
            'authorization': 'Bearer ' + accessToken
        }
        
        transport =  RequestsHTTPTransport(url=endpoint, headers=header, verify=False)
        self.client = Client(transport=transport, fetch_schema_from_transport=True)

        return

    def functions(self) -> pd.DataFrame:
        """ Get available functions"""

        graphQLString = f'''query functions {{
            functions {{
                name
                functionId
                languageVersion
                }}
            }}
        '''
    
        result = Utils._executeGraphQL(self, graphQLString)
        if result == None: return

        df = pd.json_normalize(result['functions'])
        return df

    def createFunction(self, name:str, languageVersion:str, description:str=None, files:list=None) -> str:
        """ Creates a function and returns the function Id"""

        graphQLString = f'''mutation createFunction {{
            createFunction(input:{{
                name: "{name}"
                languageVersion: {languageVersion}
                description: "{description}"

                }}) {{
                functionId
                errors {{
                    message
                    code
                    }}
                }}
            }}
        '''
    
        result = Utils._executeGraphQL(self, graphQLString)
        if result == None: return

        if result['createFunction']['errors']:
            Utils._listGraphQlErrors(result, 'createInventory')
            return

        functionId = result['createFunction']['functionId']

        if files == None: 
            logger.info(f"Function with id {functionId} created.")
            return functionId
        else:
            if type(files) != list:
                logger.error("Files must be of type list!")
            self.commitFunctionFiles(functionId, files)
            return functionId

    def commitFunctionFiles(self, functionId:str, files:list=None) -> None:
        """Upload programming files to an existing function"""

        fileList = ProgrammingUtils._upsetFiles(files)
        if fileList == None: return

        graphQLString = f'''mutation commitFunctionFiles {{
            commitFunctionFiles(input:{{
                functionId: "{functionId}"
                upsetFiles: [
                    {fileList}
                ]

                }}) {{
                errors {{
                    message
                    code
                    }}
                }}
            }}
        '''
    
        result = Utils._executeGraphQL(self, graphQLString)
        if result == None: return

        return result

    def functionFiles(self, functionId:str) -> pd.DataFrame:
        "Show function files"

        graphQLString = f''' query functionFiles {{
            functionFiles (functionId: "{functionId}") {{
                version
                files {{
                    fullname
                    }}
                }}
            }}
        '''

        result = Utils._executeGraphQL(self, graphQLString)
        if result == None: return

        df = pd.json_normalize(result['functionFiles'], meta=['version'], record_path=['files'])
        return df

    def deployFunction(self, functionId:str, functionName:str) -> str:
        """Deploys a function"""

        graphQLString = f''' mutation deployFunction {{
            deployFunction(
                input: {{
                    functionId: "{functionId}"
                    functionName: "{functionName}"
                }}
            ) {{
                deploymentId
                errors {{
                    code
                    message
                    }}
                }}
            }}
        '''

        result = Utils._executeGraphQL(self, graphQLString)
        if result == None: return

        return result

    def executeFunction(self, deploymentId:str) -> str:
        """Executes a function and returns its execution id"""

        graphQLString = f''' mutation executeFunction {{
            executeFunction(
                input: {{ 
                    deploymentId: "{deploymentId}", 
                    input: "OUTPUT" }}
            ) {{
                executionId
                result {{
                    output
                    errorMessage
                    hasError
                }}
                errors {{
                    code
                    message
                    }}
                }}
            }}
        '''

        result = Utils._executeGraphQL(self, graphQLString)
        if result == None: return

        return result


    def deleteFunction(self, functionId:str) -> None:
        """Deletes a function"""

        graphQLString = f''' mutation deleteFunction {{
            deleteFunction (input: {{
                functionId: "{functionId}"
            }}) {{
                errors {{
                    message
                }}
            }}
        }}
        '''

        result = Utils._executeGraphQL(self, graphQLString)
        if result == None: return

        return result

    def deployments(self, functionId:str) -> pd.DataFrame:

        graphQLString = f'''query deployments {{
            deployments(functionId:"{functionId}") {{
                functionAggregateId
                functionAggregateVersion
                deploymentId
                functionName
                }}
            }}
            '''
        result = Utils._executeGraphQL(self, graphQLString)
        if result == None: return

        return result