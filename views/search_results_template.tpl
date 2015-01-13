<html>
  <body>
     <H1>In search Results</H1>
     <table>
        <tr>
           <td>First Name</TD>
           <td>Last Name</td>
           <td>City</td>
           <td>State</td>
           <td>Zip</td>
        </tr>

          % for customer in results:
            <tr>
                <td>{{customer['first_name']}}</td>
                <td>{{customer['last_name']}}</td>
                <td>{{customer['city']}}</td>
                <td>{{customer['state']}}</td>
                <td>{{customer['zip']}}</td>
            </tr>
          % end
        </tr>
     </table>
   </body>
</html>