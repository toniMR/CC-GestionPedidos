# Inversión de dependencias

He realizado inversión de dependencias en el microservicio de Pedidos. Para realizarla he creado el fichero
[pgsqlDataManager.py](/src/pedidos/data_managers/pgsqlDataManager.py) que será la encargada de realizar
 todas las consultas con la base de datos de PostgreSQL. De esta forma si quisiera cambiar la BD por otra como puede
 ser MongoDB solo tendría que crear una clase en la que realice todas las operaciones con la BD de MongoDB y en el
  fichero [pedidos_rest.py](/src/pedidos/pedidos_rest.py#L35) crear un objeto de esa clase
y pasarsela a la clase gestorPedidos ([gestorPedidos.py](/src/pedidos/gestorPedidos.py#L12)), que es la que recibe el data manager.  

Una observación a tener en cuenta es que para que esto sea así de sencillo, la clase data manager de MongoDB
tendría que tener el nombre de sus operaciones igual que las del data manager que he creado para PostgreSQL, si no
tendría que cambiar el nombre de los métodos en la clase GestorPedidos.  
